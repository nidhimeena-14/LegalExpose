# import hashlib
# import os
#
#
# # Function to calculate hash of a file
# def calculate_hash(file_path, algorithm='md5'):
#     hash_func = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
#
#     with open(file_path, 'rb') as f:
#         while chunk := f.read(4096):  # Read in chunks to support large files
#             hash_func.update(chunk)
#
#     return hash_func.hexdigest()
#
# # Provide the full path to the original and tampered images
# original_path = "/home/kavita/LegalExpose/archive/TRAINING_CG-1050/TRAINING/ORIGINAL/Im1_col2.jpg"
# tampered_path = "/home/kavita/LegalExpose/archive/TRAINING_CG-1050/TRAINING/TAMPERED/Im1_col2.jpg"
#
# print(f"\n🔎 Comparing: {os.path.basename(original_path)}")
#
# # MD5
# original_md5 = calculate_hash(original_path, 'md5')
# tampered_md5 = calculate_hash(tampered_path, 'md5')
# print(f"MD5 - Original: {original_md5}")
# print(f"MD5 - Tampered: {tampered_md5}")
# print("✅ MD5 Match" if original_md5 == tampered_md5 else "❌ MD5 Mismatch (Tampered)")
#
# # SHA256
# original_sha = calculate_hash(original_path, 'sha256')
# tampered_sha = calculate_hash(tampered_path, 'sha256')
# print(f"SHA256 - Original: {original_sha}")
# print(f"SHA256 - Tampered: {tampered_sha}")
# print("✅ SHA256 Match" if original_sha == tampered_sha else "❌ SHA256 Mismatch (Tampered)")

import hashlib

def calculate_hash(file_path, algorithm='md5'):
    if algorithm == 'md5':
        hash_func = hashlib.md5()
    elif algorithm == 'sha256':
        hash_func = hashlib.sha256()
    else:
        raise ValueError("Unsupported algorithm")

    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def compare_hashes(original_path, tampered_path):
    results = {}

    original_md5 = calculate_hash(original_path, 'md5')
    tampered_md5 = calculate_hash(tampered_path, 'md5')
    results['original_md5'] = original_md5
    results['tampered_md5'] = tampered_md5

    original_sha256 = calculate_hash(original_path, 'sha256')
    tampered_sha256 = calculate_hash(tampered_path, 'sha256')
    results['original_sha256'] = original_sha256
    results['tampered_sha256'] = tampered_sha256

    results['md5_match'] = original_md5 == tampered_md5
    results['sha256_match'] = original_sha256 == tampered_sha256

    return results
