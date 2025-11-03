#!/usr/bin/python python3
"""
IDEA (International Data Encryption Algorithm) Implementation with Gradio GUI
Symmetric Block Cipher - Block size: 64 bit, Key size: 128 bit
"""

import binascii
import random
import gradio as gr

# =============================
#     Library Functions
# =============================

two_sixteen = pow(2, 16)
two_sixteen_plus_1 = two_sixteen + 1


def XOR(a, b):
    """XOR operation on two binary strings"""
    if len(a) != len(b):
        raise Exception('XOR operator unequal sizes between inputs a={} b={}'.format(len(a), len(b))) 

    result = ""
    for i in range(len(a)):
        result += '1' if a[i] != b[i] else '0'
    
    return result


def circular_left_shift(binString, k):
    """Circular left shift of binary string by k positions"""
    res = binString
    for i in range(k):
        tmp = res[0]
        res = res[1:] + tmp
    return res


def generate_subkeys(data):
    """Generate 52 subkeys from 128-bit key"""
    if len(data) != 128:
        raise Exception('generate keys function requires an input of 128 bits, but received {}'.format(len(data)))
    
    keys = []
    for i in range(7):
        subkeys = split_into_x_parts_of_y(data, 8, 16)
        keys += subkeys
        data = circular_left_shift(data, 25)
    
    return keys[:-4]


def split_into_x_parts_of_y(data, x, y):
    """Split data into x parts of y bits each"""
    res = []
    for i in range(x):
        multiplier = y * i
        start = 0 + multiplier
        stop = y + multiplier
        res.append(data[start:stop])
    return res


def generate_decrypt_keys(keys):
    """Generate decryption subkeys from encryption subkeys"""
    decrypt_keys = []
    for i in range(8):
        step = i * 6
        lower_index = 46 - step
        
        decrypt_keys.append(m_mul_inv(keys[lower_index + 2], two_sixteen_plus_1))

        tmp1 = 4
        tmp2 = 3
        if i == 0:
            tmp1 = 3
            tmp2 = 4

        decrypt_keys.append(m_sum_inv(keys[lower_index + tmp1], two_sixteen))
        decrypt_keys.append(m_sum_inv(keys[lower_index + tmp2], two_sixteen))
        
        decrypt_keys.append(m_mul_inv(keys[lower_index + 5], two_sixteen_plus_1))
        decrypt_keys.append(keys[lower_index])
        decrypt_keys.append(keys[lower_index + 1])

    decrypt_keys.append(m_mul_inv(keys[0], two_sixteen_plus_1))
    decrypt_keys.append(m_sum_inv(keys[1], two_sixteen))
    decrypt_keys.append(m_sum_inv(keys[2], two_sixteen))
    decrypt_keys.append(m_mul_inv(keys[3], two_sixteen_plus_1))

    return decrypt_keys


def m_mul_inv(a, m):
    """Multiplicative inverse modulo m using Extended Euclidean Algorithm"""
    m0 = m 
    y = 0
    x = 1
    a = int(a, 2)
    if (m == 1): 
        return 0

    while (a > 1):
        q = a // m 
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t 

    if (x < 0): 
        x = x + m0 

    bits = bin(x)[2:]
    return bits.zfill(16)


def m_sum_inv(a, m):
    """Additive inverse modulo m"""
    res = m - int(a, 2)
    bits = bin(res)[2:]
    return bits.zfill(16)


def m_mul(a, b):
    """Modular multiplication"""
    a = int(a, 2) 
    b = int(b, 2)
    res = (a * b) % two_sixteen_plus_1
    bits = bin(res)[2:]
    return bits.zfill(16)


def m_sum(a, b):
    """Modular addition"""
    a = int(a, 2) 
    b = int(b, 2)
    res = (a + b) % two_sixteen
    bits = bin(res)[2:]
    return bits.zfill(16)


def int2bits(val):
    """Convert integer to 128-bit binary string"""
    bits = bin(val)[2:]
    return bits.zfill(128)


def decode_binary_string(s):
    """Decode binary string to text"""
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s)//8))


def str_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    """Convert string to binary representation"""
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


# =============================
#     IDEA Algorithm
# =============================

def idea(block, key, mode):
    """
    IDEA encryption/decryption algorithm
    block: 64-bit binary string
    key: 128-bit binary string
    mode: 'e' for encryption, 'd' for decryption
    """
    binaryData = block
    X = split_into_x_parts_of_y(binaryData, 4, 16)

    Z = generate_subkeys(key)
    if mode == 'd':
        Z = generate_decrypt_keys(Z) 

    # 8 Rounds
    for i in range(8):
        multiplier = i * 6

        one = m_mul(X[0], Z[multiplier + 0])
        two = m_sum(X[1], Z[multiplier + 1])
        three = m_sum(X[2], Z[multiplier + 2])
        four = m_mul(X[3], Z[multiplier + 3])

        five = XOR(one, three)
        six = XOR(two, four)
        seven = m_mul(five, Z[multiplier + 4])
        eight = m_sum(six, seven)
        nine = m_mul(eight, Z[multiplier + 5])
        ten = m_sum(seven, nine)
        eleven = XOR(one, nine)
        twelve = XOR(three, nine)
        thirteen = XOR(two, ten)
        fourteen = XOR(four, ten)
        if i == 7:
            X = [eleven, thirteen, twelve, fourteen]
        else:
            X = [eleven, twelve, thirteen, fourteen]

    # Output pre-processing (half-round)    
    X[0] = m_mul(X[0], Z[48])
    X[1] = m_sum(X[1], Z[49])
    X[2] = m_sum(X[2], Z[50])
    X[3] = m_mul(X[3], Z[51])
    
    return ''.join(X)


# =============================
#     Gradio Interface Functions
# =============================

def encrypt_message(message):
    """Encrypt a message using IDEA"""
    try:
        if not message or len(message) != 8:
            return "Error: Please enter exactly 8 characters (64 bits)", ""
        
        # Convert message to binary
        data = str_to_bits(message)
        
        # Generate random 128-bit key
        private_key = int2bits(random.randint(1, pow(2, 128)))
        
        # Encrypt
        result = idea(data, private_key, "e")
        
        return f"Encrypted (binary): {result}\n\nKey (128-bit): {private_key}", private_key
    
    except Exception as e:
        return f"Error: {str(e)}", ""


def decrypt_message(encrypted_binary, key):
    """Decrypt a message using IDEA"""
    try:
        if not encrypted_binary or not key:
            return "Error: Please provide both encrypted data and key"
        
        # Remove any whitespace
        encrypted_binary = encrypted_binary.strip().replace("\n", "").replace(" ", "")
        key = key.strip().replace("\n", "").replace(" ", "")
        
        if len(encrypted_binary) != 64:
            return f"Error: Encrypted data must be exactly 64 bits (got {len(encrypted_binary)})"
        
        if len(key) != 128:
            return f"Error: Key must be exactly 128 bits (got {len(key)})"
        
        # Decrypt
        result = idea(encrypted_binary, key, "d")
        
        # Decode binary to text
        decoded = decode_binary_string(result)
        
        return f"Decrypted message: {decoded}"
    
    except Exception as e:
        return f"Error: {str(e)}"


# =============================
#     Gradio UI
# =============================

def create_interface():
    """Create Gradio interface for IDEA cipher"""
    
    with gr.Blocks(title="IDEA Cipher") as demo:
        gr.Markdown("# IDEA Cipher (International Data Encryption Algorithm)")
        gr.Markdown("**Symmetric Block Cipher** - Block size: 64 bit (8 characters) | Key size: 128 bit")
        
        with gr.Tab("Encrypt"):
            gr.Markdown("### Encrypt a Message")
            gr.Markdown("Enter exactly **8 characters** to encrypt:")
            
            with gr.Row():
                encrypt_input = gr.Textbox(
                    label="Message (8 characters)", 
                    placeholder="lalaland",
                    max_lines=1
                )
            
            encrypt_button = gr.Button("Encrypt", variant="primary")
            
            encrypt_output = gr.Textbox(
                label="Encrypted Output", 
                lines=5,
                interactive=False
            )
            
            key_storage = gr.Textbox(
                label="Key (Save this for decryption!)", 
                lines=3,
                interactive=True
            )
            
            encrypt_button.click(
                fn=encrypt_message,
                inputs=encrypt_input,
                outputs=[encrypt_output, key_storage]
            )
        
        with gr.Tab("Decrypt"):
            gr.Markdown("### Decrypt a Message")
            gr.Markdown("Enter the **64-bit encrypted binary** and the **128-bit key**:")
            
            decrypt_input = gr.Textbox(
                label="Encrypted Data (64-bit binary)", 
                placeholder="1111100001010110011001011100101000000101110010000100010001011110",
                lines=2
            )
            
            decrypt_key = gr.Textbox(
                label="Decryption Key (128-bit binary)", 
                placeholder="11001100101010000110110010010101110101010111100100011001011111101110110010000011001101010010101100000110011011101001001100111100",
                lines=3
            )
            
            decrypt_button = gr.Button("Decrypt", variant="primary")
            
            decrypt_output = gr.Textbox(
                label="Decrypted Message", 
                lines=2,
                interactive=False
            )
            
            decrypt_button.click(
                fn=decrypt_message,
                inputs=[decrypt_input, decrypt_key],
                outputs=decrypt_output
            )
        
        with gr.Tab("About"):
            gr.Markdown("""
            ### About IDEA
            
            The International Data Encryption Algorithm (IDEA) is a symmetric-key block cipher designed by James Massey and Xuejia Lai.
            
            **Key Features:**
            - Block size: 64 bits (8 characters)
            - Key size: 128 bits
            - Number of rounds: 8
            - Operations: Modular addition, multiplication, and XOR
            
            **Usage:**
            1. **Encryption**: Enter exactly 8 characters. The system generates a random 128-bit key and encrypts your message.
            2. **Decryption**: Use the encrypted binary output and the key from encryption to decrypt the message.
            
            **Note:** This implementation works on 64-bit blocks. For longer messages, you would need to implement block chaining modes.
            """)
    
    return demo


if __name__ == '__main__':
    # Create and launch the Gradio interface
    demo = create_interface()
    demo.launch(share=False)
