import hashlib


def sha256sum( filename ):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha256 = hashlib.sha256()
    with open( filename, 'rb' ) as f:
        while True:
            data = f.read( BUF_SIZE )
            if not data:
                break
            sha256.update( data )

    return sha256.hexdigest()