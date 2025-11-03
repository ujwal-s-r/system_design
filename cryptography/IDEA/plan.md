Here's a complete logical plan for building IDEA encryption from scratch with a simple Tkinter GUI:

## IDEA Algorithm Core Logic

### Step 1: Key Schedule Generation
Take the 128-bit key (16 bytes) and generate 52 subkeys of 16 bits each:[1][2]
- Split the initial 128-bit key into eight 16-bit subkeys (subkeys 1-8)
- Cyclically left shift the 128-bit key by 25 positions
- Split this shifted result into eight more 16-bit subkeys (subkeys 9-16)
- Repeat the shift-and-split process until you have all 52 subkeys[2][1]

The 25-bit shift ensures no repetition in the subkey patterns.[2]

### Step 2: Three Core Mathematical Operations
Implement these three operations that form IDEA's security foundation:[3]

**Modular Addition (mod 2^16)**: Standard addition with wraparound at 65536

**XOR Operation**: Bitwise exclusive OR

**Modular Multiplication (mod 2^16+1)**: Multiplication with wraparound at 65537, treating 0 as 65536 for the multiplication operation

### Step 3: Single Round Structure
Each of the 8 rounds processes four 16-bit blocks (X1, X2, X3, X4) using 6 subkeys:[2]

1. Multiply X1 with subkey 1 (mod 2^16+1)
2. Add X2 with subkey 2 (mod 2^16)
3. Add X3 with subkey 3 (mod 2^16)
4. Multiply X4 with subkey 4 (mod 2^16+1)
5. XOR results from steps 1 and 3
6. XOR results from steps 2 and 4
7. Multiply result from step 5 with subkey 5 (mod 2^16+1)
8. Add results from steps 6 and 7 (mod 2^16)
9. Multiply result from step 8 with subkey 6 (mod 2^16+1)
10. Add results from steps 7 and 9 (mod 2^16)
11. XOR results from steps 1 and 9
12. XOR results from steps 3 and 9
13. XOR results from steps 2 and 10
14. XOR results from steps 4 and 10

After each round (except the last), swap the middle two blocks (X2 and X3).[3]

### Step 4: Final Half-Round (Output Transformation)
After 8 complete rounds, apply a final transformation using the last 4 subkeys:[2]
1. Multiply X1 with subkey 49 (mod 2^16+1)
2. Add X2 with subkey 50 (mod 2^16)
3. Add X3 with subkey 51 (mod 2^16)
4. Multiply X4 with subkey 52 (mod 2^16+1)

Concatenate all four blocks to produce the 64-bit ciphertext.

### Step 5: Decryption Logic
For decryption, use the **inverse subkeys** in reverse order:[1]
- Multiplicative inverses (mod 2^16+1) for multiplication subkeys
- Additive inverses (mod 2^16) for addition subkeys
- XOR subkeys remain the same (self-inverse)

Apply the same round structure with these inverse subkeys.

## Module Structure Plan

**Module 1: Mathematical Operations**
- Function: mod_multiply(a, b) - handles modular multiplication mod 2^16+1
- Function: mod_add(a, b) - handles modular addition mod 2^16
- Function: xor(a, b) - bitwise XOR
- Function: multiplicative_inverse(x) - for decryption key generation

**Module 2: Key Schedule**
- Function: generate_encryption_subkeys(key_128bit) - returns list of 52 subkeys
- Function: generate_decryption_subkeys(encryption_subkeys) - returns inverse subkeys
- Helper: circular_left_shift(bits, positions)
- Helper: split_into_16bit_blocks(128bit_data)

**Module 3: Encryption/Decryption Core**
- Function: idea_round(X1, X2, X3, X4, subkeys_for_round) - processes one round
- Function: output_transformation(X1, X2, X3, X4, final_4_subkeys)
- Function: idea_encrypt(plaintext_64bit, key_128bit) - main encryption
- Function: idea_decrypt(ciphertext_64bit, key_128bit) - main decryption

**Module 4: Data Handling**
- Function: text_to_64bit_blocks(text) - converts strings to 64-bit blocks with padding
- Function: blocks_to_text(blocks) - converts back and removes padding
- Function: bytes_to_hex(data) - for display
- Function: hex_to_bytes(hex_string) - for input processing

## GUI Structure Plan

**Main Window Components**:
- Title label at top
- Key input section with text entry (accepts hex string representing 128 bits)
- Button to generate random 128-bit key
- Left panel for encryption with plaintext textarea, "Encrypt" button, ciphertext display
- Right panel for decryption with ciphertext textarea, "Decrypt" button, plaintext display
- Status bar at bottom for error messages

**GUI Flow**:
1. User enters or generates 128-bit key in hex format
2. For encryption: user types plaintext, clicks encrypt, sees hex ciphertext
3. For decryption: user pastes hex ciphertext, clicks decrypt with same key, sees original text
4. Include validation for key length and ciphertext format

## Implementation Order

1. Build the three mathematical operations first (test with known values)
2. Implement key schedule generation (verify 52 subkeys are unique)
3. Code the single round transformation (test with test vectors)
4. Complete 8 rounds plus output transformation
5. Add decryption with inverse subkeys
6. Build data conversion utilities (text ↔ blocks ↔ hex)
7. Create basic Tkinter window with input/output fields
8. Connect GUI buttons to encryption/decryption functions
9. Add error handling and user feedback

This pure Python implementation will be around 300-400 lines total without any external cryptography libraries.[3][1][2]

