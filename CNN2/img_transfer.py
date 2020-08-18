import os, shutil

# Fresh Organges Directory
original_train_freshoranges_dir = 'datasets/train/freshoranges'
original_test_freshoranges_dir = 'datasets/test/freshoranges'

# Rotten Oranges Directory
original_train_rottenoranges_dir = 'datasets/train/rottenoranges'
original_test_rottenoranges_dir = 'datasets/test/rottenoranges'

# Base Directory
base_dir = 'subsets'
os.mkdir(base_dir)

# Train, Validation, Test Directories
train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

# Train Oranges Directories
train_fresh_oranges = os.path.join(train_dir, 'fresh_oranges')
os.mkdir(train_fresh_oranges)

train_rotten_oranges = os.path.join(train_dir, 'rotten_oranges')
os.mkdir(train_rotten_oranges)

# Validation Oranges Directories
validation_fresh_oranges = os.path.join(validation_dir, 'fresh_oranges')
os.mkdir(validation_fresh_oranges)

validation_rotten_oranges = os.path.join(validation_dir, 'rotten_oranges')
os.mkdir(validation_rotten_oranges)

# Test Oranges Directories
test_fresh_oranges = os.path.join(test_dir, 'fresh_oranges')
os.mkdir(test_fresh_oranges)

test_rotten_oranges = os.path.join(test_dir, 'rotten_oranges')
os.mkdir(test_rotten_oranges)

# Transfer First 1000 Fresh Oranges Train Files
src_list = os.listdir(original_train_freshoranges_dir)
src = []
for i in range(1000):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_train_freshoranges_dir, file)
    shutil.copy(full_path, train_fresh_oranges)

# Transfer Next 400 Fresh Oranges Train Files
src = []
for i in range(1000,1400):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_train_freshoranges_dir, file)
    shutil.copy(full_path, validation_fresh_oranges)

# Transfer First 300 Fresh Oranges Test Files
src_list = os.listdir(original_test_freshoranges_dir)
src = []
for i in range(300):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_test_freshoranges_dir, file)
    shutil.copy(full_path, test_fresh_oranges)

# Transfer First 1000 Rotten Oranges Train Files
src_list = os.listdir(original_train_rottenoranges_dir)
src = []
for i in range(1000):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_train_rottenoranges_dir, file)
    shutil.copy(full_path, train_rotten_oranges)

# Transfer Next 400 Rotten Oranges Train Files
src = []
for i in range(1000,1400):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_train_rottenoranges_dir, file)
    shutil.copy(full_path, validation_rotten_oranges)

# Transfer First 300 Rotten Oranges Test Files
src_list = os.listdir(original_test_rottenoranges_dir)
src = []
for i in range(300):
    src.append(src_list[i])
for file in src:
    full_path = os.path.join(original_test_rottenoranges_dir, file)
    shutil.copy(full_path, test_rotten_oranges)
