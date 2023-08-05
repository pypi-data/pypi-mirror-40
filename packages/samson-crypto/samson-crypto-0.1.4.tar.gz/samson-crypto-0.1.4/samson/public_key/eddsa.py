from samson.utilities.bytes import Bytes
from samson.public_key.dsa import DSA
from samson.utilities.ecc import EdwardsCurve25519, TwistedEdwardsPoint, TwistedEdwardsCurve
from samson.hashes.sha2 import SHA512
from samson.encoding.pem import pem_decode, pem_encode

from samson.encoding.openssh.eddsa_private_key import EdDSAPrivateKey
from samson.encoding.openssh.eddsa_public_key import EdDSAPublicKey
from samson.encoding.openssh.openssh_private_header import OpenSSHPrivateHeader
from samson.encoding.openssh.kdf_params import KDFParams

import base64

def bit(h,i):
  return (h[i//8] >> (i%8)) & 1

# https://ed25519.cr.yp.to/python/ed25519.py
class EdDSA(DSA):
    """
    Edwards Curve Digitial Signature Algorithm
    """

    def __init__(self, curve: TwistedEdwardsCurve=EdwardsCurve25519, hash_obj: object=SHA512(), d: int=None, A: TwistedEdwardsPoint=None, a: int=None):
        """
        Parameters:
            curve (TwistedEdwardsCurve): Curve used for calculations.
            hash_obj           (object): Instantiated object with compatible hash interface.
            d                     (int): Private key.
            A     (TwistedEdwardsPoint): (Optional) Public point.
            a                     (int): (Optional) Public scalar.
        """
        self.B = curve.B
        self.curve = curve
        self.d = Bytes.wrap(d or max(1, Bytes.random(hash_obj.digest_size).int()))
        self.H = hash_obj

        self.h = hash_obj.hash(self.d)

        self.a = a or 2**(curve.n) | sum(2**i * bit(self.h, i) for i in range(curve.c, curve.n))
        self.A = A or self.B * self.a



    def __repr__(self):
        return f"<EdDSA: d={self.d}, A={self.A}, curve={self.curve}, H={self.H}>"

    def __str__(self):
        return self.__repr__()


    def encode_point(self, P: TwistedEdwardsPoint) -> Bytes:
        """
        Encodes a `TwistedEdwardsPoint` as `Bytes`.

        Parameters:
            P (TwistedEdwardsPoint): Point to encode.
        
        Returns:
            Bytes: `Bytes` encoding.
        """
        x, y = P.x, P.y
        return Bytes(((x & 1) << self.curve.b-1) + ((y << 1) >> 1), 'little').zfill(self.curve.b // 8)



    def decode_point(self, in_bytes: Bytes) -> TwistedEdwardsPoint:
        """
        Decodes `Bytes` to a `TwistedEdwardsPoint`.

        Parameters:
            in_bytes (Bytes): `TwistedEdwardsPoint` encoded as `Bytes`.
        
        Returns:
            TwistedEdwardsPoint: Decoded point.
        """
        y_bytes = Bytes([_ for _ in in_bytes], 'little')
        y_bytes[-1] &= 0x7F
        y = y_bytes.int()
        x = self.curve.recover_point_from_y(y).x

        if (x & 1) != bit(in_bytes, self.curve.b-1):
            x = self.curve.q - x

        return TwistedEdwardsPoint(x, y, self.curve)



    def sign(self, message: bytes) -> (int, int):
        """
        Signs a `message`.

        Parameters:
            message (bytes): Message to sign.
            k         (int): (Optional) Ephemeral key.
        
        Returns:
            (int, int): Signature formatted as (r, s).
        """
        r = self.H.hash(self.curve.magic + self.h[self.curve.b//8:] + message)[::-1].int()
        R = self.B * (r % self.curve.l)
        eR = self.encode_point(R)
        k = self.H.hash(self.curve.magic + eR + self.encode_point(self.A) + message)[::-1].int()
        S = (r + (k % self.curve.l) * self.a) % self.curve.l
        return eR + Bytes(S, 'little').zfill(self.curve.b//8)



    def verify(self, message: bytes, sig: (int, int)) -> bool:
        """
        Verifies a `message` against a `sig`.

        Parameters:
            message  (bytes): Message.
            sig ((int, int)): Signature of `message`.
        
        Returns:
            bool: Whether the signature is valid or not.
        """
        sig = Bytes.wrap(sig, 'little')

        if len(sig) != self.curve.b // 4:
            raise ValueError("`sig` length is wrong.")

        R = self.decode_point(sig[:self.curve.b//8])
        S = sig[self.curve.b//8:].int()

        h = self.H.hash(self.curve.magic + self.encode_point(R) + self.encode_point(self.A) + message)[::-1].int()

        return self.B * S == R + (self.A * h)



    @staticmethod
    def import_key(buffer: bytes, passphrase: bytes=None):
        """
        Builds an EdDSA instance from DER and/or PEM-encoded bytes.

        Parameters:
            buffer     (bytes): DER and/or PEM-encoded bytes.
            passphrase (bytes): Passphrase to decrypt DER-bytes (if applicable).
        
        Returns:
            EdDSA: EdDSA instance.
        """
        if buffer.startswith(b'----'):
            buffer = pem_decode(buffer, passphrase)

        ssh_header = b'ssh-ed25519'

        if ssh_header in buffer:
            # SSH private key?
            if b'openssh-key-v1' in buffer:
                header, left_over = OpenSSHPrivateHeader.unpack(buffer)
                pub, left_over = EdDSAPublicKey.unpack(left_over)

                decryptor = None
                if passphrase:
                    decryptor = header.generate_decryptor(passphrase)

                priv, _left_over = EdDSAPrivateKey.unpack(left_over, decryptor)
                a, d = priv.a, priv.d

            else:
                if buffer.split(b' ')[0][:len(ssh_header)] == ssh_header:
                    buffer = base64.b64decode(buffer.split(b' ')[1])

                pub, _ = EdDSAPublicKey.unpack(buffer, already_unpacked=True)
                a, d = pub.a, 0
        else:
            raise ValueError("Unable to parse provided EdDSA key.")

        eddsa = EdDSA(curve=EdwardsCurve25519, d=d, a=a)

        return eddsa


    def export_private_key(self, encode_pem: bool=True, encoding: str='OpenSSH', marker: str=None, encryption: str=None, passphrase: bytes=None, iv: bytes=None) -> bytes:
        """
        Exports the full EdDSA instance into encoded bytes.

        Parameters:
            encode_pem  (bool): Whether or not to PEM-encode as well.
            encoding     (str): Encoding scheme to use. Currently supports 'OpenSSH'.
            marker       (str): Marker to use in PEM formatting (if applicable).
            encryption   (str): (Optional) RFC1423 encryption algorithm (e.g. 'DES-EDE3-CBC').
            passphrase (bytes): (Optional) Passphrase to encrypt DER-bytes (if applicable).
            iv         (bytes): (Optional) IV to use for CBC encryption.
        
        Returns:
            bytes: Bytes-encoded EdDSA instance.
        """
        if encoding.upper() == 'OpenSSH'.upper():
            if encryption:
                kdf_params = KDFParams('kdf_params', iv or Bytes.random(16), 16)
            else:
                kdf_params = KDFParams('kdf_params', b'', b'')

            header = OpenSSHPrivateHeader(
                header=OpenSSHPrivateHeader.MAGIC_HEADER,
                encryption=encryption or b'none',
                kdf=b'bcrypt' if encryption else b'none',
                kdf_params=kdf_params,
                num_keys=1
            )

            public_key = EdDSAPublicKey('public_key', self.a)
            private_key = EdDSAPrivateKey(
                'private_key',
                check_bytes=None,
                a=self.a,
                d=self.d,
                host=b'nohost@localhost'
            )

            encryptor, padding_size = None, 8
            if passphrase:
                encryptor, padding_size = header.generate_encryptor(passphrase)

            packed_key = header.pack() + EdDSAPublicKey.pack(public_key) + EdDSAPrivateKey.pack(private_key, encryptor, padding_size)
            if encode_pem:
                encoded = pem_encode(packed_key, marker or 'OPENSSH PRIVATE KEY')
        else:
            raise ValueError(f'Unsupported encoding "{encoding}"')

        return encoded


    def export_public_key(self, encode_pem: bool=None, encoding: str='OpenSSH', marker: str=None) -> bytes:
        """
        Exports the only the public parameters of the EdDSA instance into encoded bytes.

        Parameters:
            encode_pem (bool): Whether or not to PEM-encode as well.
            encoding    (str): Encoding scheme to use. Currently supports 'OpenSSH', and 'SSH2'.
            marker      (str): Marker to use in PEM formatting (if applicable).
        
        Returns:
            bytes: Encoding of EdDSA instance.
        """
        if encoding == 'OpenSSH':
            public_key = EdDSAPublicKey('public_key', self.a)
            encoded = b'ssh-ed25519 ' + base64.b64encode(EdDSAPublicKey.pack(public_key)[4:]) + b' nohost@localhost'
            default_pem = False

        elif encoding == 'SSH2':
            public_key = EdDSAPublicKey('public_key', self.a)
            encoded = EdDSAPublicKey.pack(public_key)[4:]
            default_marker = 'SSH2 PUBLIC KEY'
            default_pem = True
        else:
            raise ValueError(f'Unsupported encoding "{encoding}"')

        if (encode_pem is None and default_pem) or encode_pem:
            encoded = pem_encode(encoded, marker or default_marker)

        return encoded
