from pathlib import Path
import hashlib

CHUNKS = [
    (5000, 'H4sIAAAAAAAAA+w8/XfTVpb87L9CNT0zBJATh49MvZ1SSjltzjBtNqW7ZzcJtmLL'.encode(), '70a552d8f7c23efcb88e2ba8a63b5d20db1d4ca8f1f21ecc0eff64120e99df52'),
    (5000, 'glQTrAlSnTjhdnFjIbF2QJlgc8yQjrJiKeSvJGJSk27nno8/kqH0IZ3OkFhmxEhJ'.encode(), '454038ab9f6f83a9714cce21f5acfcd81226ec0a95d2a49e6d372d358a045000'),
    (5000, 'ATLA0plsxEAFJpy+I7eKp29QqaR+G0Ly/iYd338gG8nE/zMWiX0S6yWUJQKkrBms'.encode(), '39634a451a3ede551a780605b9f792c2ee88b9d6f626621ca2ae57a9e5012919'),
    (5000, 'Ba5okgbz694IUK8VB5dHcwMwXckWlHom7HfaX6dSCCuME9gMXR9X4AnxhfrZutAB'.encode(), '3191571b75b0ecbdaf8eabd83061b6de102676ff890f5d17b3fbf214cae5988b'),
    (5000, '/JNY3+8bOMGVy38SYF8E5mP7qI+tDeClnAK7zqGdM7Jw57vi038Y5CMQOEw7YRME'.encode(), 'c9929fe20872590b7e3f0e904a2048b82330f9a5eb9f80c306899a6de57fede2'),
    (5000, '3xEDFdXl6IxMpXGAJ60BUu6zzmKrKwFGcs8Y9F4MpeIZkhvmLoMdq14tIX2GmdWC'.encode(), 'c7b0853c4233fc8305c1d32ad37b76865c6d77e3d5f8a9f0251385a29ef1da1f'),
    (5000, 'n72xcC0Pf/6NNJFD1PjBaH6qS98rsLgABeMv27v/+O727X8MJL0+QLWzORiTdvGY'.encode(), '93932db105ee82f0da6e91542b7292bfc32629bac02d06610d173f9499cf9b44'),
    (5000, 'pSd7KJk9YJ+2tY5n5tkYbF4EaIsmQescOOSNTtlXv3B51dv30St0FIGwkb+0v+c/'.encode(), 'bc849c9e58789768939038856da489fc2e9e1d99f666a1d16f5bcfd68be2d9a5'),
    (5000, 'Y6GeHI7z98rjx8h5RxFnTjP7Ypbh8Ag4kDWPCcxwZwoYFU+Y86EmrmRlTYmLPjyj'.encode(), 'ce0c981c0e082f72f9f8190518c5629c7f213e9a4998d86a6631da1c727e716b'),
    (5000, 'bIPA/klMl1yeF1GXXC+lM/3KgerJJSDUktF4pe5ndWTJq63TqrcyuzEKcK7/RsXR'.encode(), '8f71fbff6051a761f9372bd808592af03e65c422f7422eb7673052956e05bdf6'),
    (5000, '2dhABr5TfR33x7JNjfRhYxgZ6Nu1DupUNZOBX+PSgRQyfsG+Q5RiHToNVCo+oyv7'.encode(), 'c5e5ae62d678bf7e919f4d68878438a60354076fbc5902ec460a679935ada4b5'),
    (5000, 'AgRE62noNXqGEAzGuAGY9N9U8FL2+z+W90uNPvXeXrh5DLt8XfrG7C7o2uUqC33P'.encode(), '37c4f5ee2ff633acf24b7a1a4c93532d969a885e342d4374f9fa0625875dc5cc'),
    (5000, 'OETmNPr0qbNBf4hbtVJCjlFOvvpemrmR79EHOzoOHB02VCodc2TghIrLnLVG1h5e'.encode(), '483fcaeb13262e55e2082b986a8038919a379007181aa89e4c22c553cbb9e5c5'),
    (5000, '7HXIKEbGrSCiag8e1yGi9IqADaETYkFUENJWcXx6/ulliqbIHsMw2OnpxeGjtM28'.encode(), 'aeae23b6b938283e94a09cdd5c89f3c6bef60f07dcf100b56e090db53c63b324'),
    (5000, 'M0SBsJU9aygVY4wrkW7oNh38kxzgpQmuQL2hOja+2YHQfARTdMmm9fvb/9zZva19'.encode(), '1f1072b70b90c0a9441e345a762eab7c0a22c59dc554581a27d16da1568ab18f'),
    (5000, '6mpRC3eUIha69ZJZ+ovItC2VlAHCOd8fQzrhrbAL8C7jC9lBzQMf9cXTTbKdhCCx'.encode(), 'cb9908724daada3ca90c1fcca5a49f82e005a2cfe040fa14536c62e8d459b352'),
    (5000, 'qjVdpRxG73Z2oSb2oWkTcrzTZJZzXKQHDi9CrnHRDHsZQnWc6m42yz/g1Y3C/WfB'.encode(), '9f7b008233a232f449f6bd8b80cd41119742a3363a79d58f975b17e574a7fad6'),
    (5000, 'qeo7EE0jxpdxos1USM99XuebRJmtm/W91ctjX1SOcSi7emlJxgYLC88zNkhp2ZF1'.encode(), 'a263399b51f7be864b65f804b087a20418a7cbbbe5329b1ec9b231916e03c89f'),
    (5000, 'EGQRQeSQP6xJq1dNK6IIQfI7upENU7Pw8+5gnwKWsGEb8xTWk4XFDTCIq6BZkq6h'.encode(), '833acb20fabc10a3fac221d33b68e3a7cebd3ba57a314c339276a49a21c97fd9'),
    (5000, '8tWbnbVXn/+s+EEzFSvzwxz0C41LN54T58Pe8IvZZ26tPQndrneTNzcQ4Y31LzQ3'.encode(), 'f762904855212ba95a5825e67194be8e8ec3a428168104befc211447d62138eb'),
    (5000, '0Am80iyZCSUQ9xFiv+UgG8cbhGdg5K3ScnCTQjaovb4oZioDFBc53bcC/oIs2yu8'.encode(), '1e4278ba47e85ebfaa218ea1161e9edb6094a5af764280e223fec66beabc5942'),
    (5000, 'UyE1Ga9zIrQktuKgxV+zYOWiSuF2fRPVfjc9MQNmKxNUZVLVw4jrNjqjWDOmopV0'.encode(), '2054c9f56a7e34919803e50728e0235ceed9ce745e36b8be6e3f28252263c66b'),
    (4288, 'rXUvXpGErs0WJI6Zg6DBDOzVE2cqqMN7loXJEEfXi9BvIAnIYBQfGlioMRmGBkHW'.encode(), '8fdb4b80f29908e784c7908d09822aff7c6ea58fb1f85b5b184ebd260401c8c4'),
]

sources = [(p, p.read_bytes()) for p in sorted(Path('.bootstrap').glob('issue20.part.*'))]
output = bytearray()
for index, (length, prefix, expected) in enumerate(CHUNKS):
    found = None
    for path, data in sources:
        start = 0
        while True:
            position = data.find(prefix, start)
            if position < 0:
                break
            candidate = data[position : position + length]
            if len(candidate) == length and hashlib.sha256(candidate).hexdigest() == expected:
                found = candidate
                break
            start = position + 1
        if found is not None:
            break
    if found is None:
        raise SystemExit(f'missing verified payload chunk {index}')
    output.extend(found)
if len(output) != 114288:
    raise SystemExit(f'unexpected payload length: {len(output)}')
Path('/tmp/issue20.b64').write_bytes(output)
print('reconstructed payload base64:', len(output))
