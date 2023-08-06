import struct
import binascii
import json
import time
stratum_examples = (
    b'{"params":["1c9761","b59dd3eb0d789176dff16db129b1e928727cc0a7001e65250000000000000000","01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4503fb6f08fabe6d6d552995d31269a2d466d7ba999ca633c2bac0590aa003da3c41fb37d23278783c0100000000000000","61971c2f736c7573682f0000000003880f0a4c000000001976a9147c154ed1dc59609e3d26abb2df2ea3d587cd8c4188ac00000000000000002c6a4c2952534b424c4f434b3afad0c31938e4ad0307058d9612961d355eba7c5914c9e29467350fb05bd94c2b0000000000000000266a24aa21a9ed0af0e66255b580d66ed04ec6577e0656f520bd55b0e50bfa674f7f00e334ee7000000000",["a78453839e2d497d2f50c7abfa6c0500ab7708c0a3e754bc87f53dc0e4e349c8","d2e5a8bd8ecb96b3727536cd8b3c863836031b3e95a7039253cf371ff50782c1","1ba39188094978c1c5ba14ea20b3534c692d8b8b27895ae07cf5404b938ff571","da67ed489f77bdac469f6504e63f1b324f2764bef3d75c63001e8db75e60767a","65ebc33a2efffdd82580094739a17e9f8f0d255589f5d663dd9bfbffbebf9135","6385cc8e30aca36b0506087becd7054306dd7a3bad348de990c778ac8f9a5f41","a266dd0074b39d42b40133c4d5b27f15bb144fca25b82ff1f5e58e73e47dca08","873b1ea3dd2c1fe9affaf9e2a4004a5c8cb44716e2ed0c318e02d3800aff42d6","b5fd767af7751abdd054dfd066a4a84fa4ed59ffea5d9ed9274f1ab507a35c35","82e497e678c0fd155b5a5aaec53fff3ccb2e2d27b111721ca6d26d510060fafc","57669fe4bf995b3270043bd258fa19500ba08607f1df69d8c7728cceb5a82010","1e1fa0ff8edc2312b575c728fd433ec481db4521d560d5097458bea301318c3d"],"20000000","1731d97c","5c0b1314",false],"id":null,"method":"mining.notify"}',
    b'{"params":["1c9765","b59dd3eb0d789176dff16db129b1e928727cc0a7001e65250000000000000000","01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4503fb6f08fabe6d6d552995d31269a2d466d7ba999ca633c2bac0590aa003da3c41fb37d23278783c0100000000000000","65971c2f736c7573682f000000000338d20f4c000000001976a9147c154ed1dc59609e3d26abb2df2ea3d587cd8c4188ac00000000000000002c6a4c2952534b424c4f434b3ae284c873d1e0cceb088f80b673be67aed4baee0d2bfae9885573f5f8120f43510000000000000000266a24aa21a9edebe54c0c201e1d61d74ce7e0170ee198bf021a34e735651e486bbacc1228e4ec00000000",["a78453839e2d497d2f50c7abfa6c0500ab7708c0a3e754bc87f53dc0e4e349c8","d2e5a8bd8ecb96b3727536cd8b3c863836031b3e95a7039253cf371ff50782c1","1ba39188094978c1c5ba14ea20b3534c692d8b8b27895ae07cf5404b938ff571","da67ed489f77bdac469f6504e63f1b324f2764bef3d75c63001e8db75e60767a","65ebc33a2efffdd82580094739a17e9f8f0d255589f5d663dd9bfbffbebf9135","15bbed3325e8d025dfc0770d5820d60793494a152268d6037c58c8a423f2fdd3","5f742578294bb1e3cdd8b58ab620354c4533f34c7fb5420e815a2a9fbb857059","c09cd3a07b5555d300022c89c77bb76944c179e9ace25e765cb17efe5f291995","14e6a0e21a4cfdf76ca79949ccb8648ab28e872caadbb2c7307870145ca09e7e","e46c1b3c9df28f586df2e24994aebb3d22a67a7ecb03eb7981c896dd9e9546dc","24fe8ba89beae2ccd1ac36225c1142cbc26db02ba8a34a4149c8b766ffb78a32","075d5c146fad43b0999d8c497d8c5e2f5c56556cc5eced0b469ec401de30adea"],"20000000","1731d97c","5c0b1350",false],"id":null,"method":"mining.notify"}',
    b'{"params":["1c9767","b59dd3eb0d789176dff16db129b1e928727cc0a7001e65250000000000000000","01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4503fb6f08fabe6d6d552995d31269a2d466d7ba999ca633c2bac0590aa003da3c41fb37d23278783c0100000000000000","67971c2f736c7573682f00000000036ca4134c000000001976a9147c154ed1dc59609e3d26abb2df2ea3d587cd8c4188ac00000000000000002c6a4c2952534b424c4f434b3ab31c0983ecb8ec096105f4dc8deb3f94a9b18c8d88cdfc3099c4c9c123fc9dbf0000000000000000266a24aa21a9ed82dbd5cf6a4800539530e09e07ee09e62118aebfdf95f6f97429b2964dcd9d4d00000000",["a78453839e2d497d2f50c7abfa6c0500ab7708c0a3e754bc87f53dc0e4e349c8","d2e5a8bd8ecb96b3727536cd8b3c863836031b3e95a7039253cf371ff50782c1","1ba39188094978c1c5ba14ea20b3534c692d8b8b27895ae07cf5404b938ff571","da67ed489f77bdac469f6504e63f1b324f2764bef3d75c63001e8db75e60767a","d9608576da19bb998994c1e89ffd8d70e54932db60c418a307bf12ec2d650647","ee324eb5e59d5a8066dff2138f451955893ff39b74f8e646981dfd052737b8b4","4a7dadc2a6920bff6f64c4eee3d5679d11393f09d3c549d5815390a2d9affa93","24859e95c2b42771a43f71e21e0c56da91f16020c310b0af98fb29840f0e118b","1a52a840e3e5fc23b994ccd51206bc320e4f6a5ea226a5cd987cc2b933109b79","3d1e02905030ec0985d675dac94a22448ab1e69b10d72a0559fc8b7160fb3772","dcfe6f4313453cedc22e13c4b6ddaf55079997388e2dcd90e7fa2d4ce1922b72","9d17ae464c37169b3cca411256a9bb9210cb37dc813755e50ec9931bd8d46805"],"20000000","1731d97c","5c0b136e",false],"id":null,"method":"mining.notify"}'
)
(job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs) = params[:9]




def build_merkle_root(coinbase_hash, merkle_branch):
    merkle_root = coinbase_hash
    for h in merkle_branch:
        merkle_root = doublesha(merkle_root + h)
    return merkle_root

def extranonce2_padding(extranonce2, extranonce2_size):
    '''Return extranonce2 with padding bytes'''

    if not extranonce2_size:
        raise Exception("Extranonce2_size isn't set yet")

    extranonce2_bin = struct.pack('>I', extranonce2)
    missing_len = extranonce2_size - len(extranonce2_bin)

    if missing_len < 0:
        # extranonce2 is too long, we should print warning on console,
        # but try to shorten extranonce2
        print(
            "Extranonce size mismatch. Please report this error to pool operator!")
        return extranonce2_bin[abs(missing_len):]

    # This is probably more common situation, but it is perfectly
    # safe to add whitespaces
    return b'\x00' * missing_len + extranonce2_bin

def stratum_to_getwork(stratum_msg):
    extranonce2 = 0

    '''Build job object from Stratum server broadcast'''
    stratum_msg = json.loads(stratum_msg)
    (job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime,
     clean_jobs) = stratum_msg['params'][:9]

    #job = Job()
    #job.job_id = job_id
    # job.prevhash = prevhash
    coinb1_bin = binascii.unhexlify(coinb1)
    coinb2_bin = binascii.unhexlify(coinb2)
    merkle_branch = [binascii.unhexlify(tx) for tx in merkle_branch]
    #job.version = version
    #job.nbits = nbits
    ntime_delta = int(ntime, 16) - int(time.time())

    #extranonce2 = increase_extranonce2()
    extranonce2 += 1

    # 2. Build final extranonce
    # extranonce = build_full_extranonce(extranonce2)
    # _, extranonce1, extranonce2_size = (yield f.rpc('mining.subscribe', []))[:3]
    extranonce1_bin = binascii.unhexlify(extranonce1)
    '''Join extranonce1 and extranonce2 together while padding
    extranonce2 length to extranonce2_size (provided by server).'''
    extranonce = extranonce1_bin + extranonce2_padding(extranonce2)

    # def serialize_header(ntime, nonce):
    # 3. Put coinbase transaction together
    coinbase_bin = build_coinbase(extranonce)

    # 4. Calculate coinbase hash
    coinbase_hash = doublesha(coinbase_bin)
    # 6. Generate current ntime
    ntime = int(time.time()) + ntime_delta
    merkle_root = binascii.hexlify(reverse_hash(build_merkle_root(coinbase_hash, merkle_branch)))

    r = version
    r += prevhash
    r += merkle_root
    r += binascii.hexlify(struct.pack('>I', ntime))
    r += nbits
    r += binascii.hexlify(struct.pack('>I', nonce))
    r += '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'  # padding
    return r
