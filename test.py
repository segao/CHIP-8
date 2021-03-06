import mychip8

# 0x00E0 - clear_screen()
def test_0x00E0(chip8):
    chip8.initialize() # Reset values
    for pixel in range(len(chip8.screen_pixel_states)):
        chip8.screen_pixel_states[pixel] = 1 # Set screen to white
    chip8.clear_screen() # Run opcode
    
    for pixel in range(len(chip8.screen_pixel_states)):
        if (chip8.screen_pixel_states[pixel] != 0): # If screen is not cleared
            return 0 # Return false
    return 1

# 0x00EE - return_address()
def test_0x00EE(chip8):
    chip8.initialize() # Reset values
    chip8.stack.append(0x0DEA) # Push a return address to stack
    chip8.return_address() # Run opcode
    
    if chip8.program_counter != 0x0DEA: # If pc returns a different address
        return 0 # Return false
    return 1

# 0x1NNN - jump_address()
def test_0x1NNN(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x1121 # Set opcode
    chip8.jump_address() # Run opcode
    
    if chip8.program_counter != 0x121: # If pc is not set to address
        return 0 # Return false
    return 1

# 0x2NNN - call_subroutine()
def test_0x2NNN(chip8):
    chip8.initialize() # Reset values
    chip8.call_subroutine() # Run opcode
    chip8.operation_code = 0x2121
    #print(hex(chip8.stack.pop()))
    #print(hex(chip8.program_counter))
    
    if chip8.stack.pop() != 0x202 and chip8.program_counter != 0x121: # If pc is not pushed to stack or pc is not set to address
        return 0 # Return false
    return 1

# 0x3XNN - skip_if_equal(), 
# Unequal case
def test_0x3XNN_unequal(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x3121
    chip8.x = 0x1 # Set x
    
    chip8.skip_if_equal() # Run opcode
    if chip8.program_counter != 0x202: # If pc is not incremented by 2
        return 0 # Return false
    return 1

# 0x3XNN - skip_if_equal()
# Equal case
def test_0x3XNN_equal(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x3121
    chip8.x = (chip8.operation_code & 0x0F00) >> 8 # Set x

    chip8.V[chip8.x] = chip8.operation_code & 0x00FF # Set pc to equal
    chip8.skip_if_equal() # Run opcode
    if chip8.program_counter != 0x204: # If pc is not incremented by 4
        return 0 # Return false
    return 1

# 0x4XNN - skip_if_unequal()
# Unequal case
def test_0x4XNN_unequal(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x4121
    chip8.x = 0x1 # Set x
    
    chip8.skip_if_unequal() # Run opcode
    if chip8.program_counter != 0x204: # If pc is not incremented by 4
        return 0 # Return false
    return 1

# 0x4XNN - skip_if_equal()
# Equal case
def test_0x4XNN_equal(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x4121
    chip8.x = 0x1 # Set x
    
    chip8.V[chip8.x] = chip8.operation_code & 0x00FF # Set pc to equal
    chip8.skip_if_unequal() # Run opcode
    if chip8.program_counter != 0x202: # If pc is not incremented by 2
        return 0 # Return false
    return 1

# 0x5XY0 - skip_if_registers_equal()
# Unequal case
def test_0x5NNN_unequal(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10
    chip8.V[chip8.y] = 0x20
    
    chip8.skip_if_registers_equal() # Run opcode
    if chip8.program_counter != 0x202: # If pc is not incremented by 2
        return 0 # Return false
    return 1
    
# 0x5NNN - skip_if_registers_equal()
# Equal case
def test_0x5NNN_equal(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10
    chip8.V[chip8.y] = 0x10
    
    chip8.skip_if_registers_equal() # Run opcode
    if chip8.program_counter != 0x204: # If pc is not incremented by 2
        return 0 # Return false
    return 1

# 0x6XNN - set_register_value()
def test_0x6XNN(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x6121 
    chip8.x = (chip8.operation_code & 0x0F00) >> 8 # Set x
    
    chip8.set_register_value() # Run opcode
    if chip8.V[chip8.x] != 0x21: # If V[x] != NN
        return 0 # Return false
    return 1

# 0x7XNN - register_add_value()
def test_0x7XNN(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0x7121
    chip8.x = (chip8.operation_code & 0x0F00) >> 8 # Set x
    chip8.V[chip8.x] = 0x121
    
    chip8.register_add_value() # Run opcode
    if chip8.V[chip8.x] != (0x121 + 0x21):
        return 0
    return 1

# 0x8XY0 - set_X_to_Y()
def test_0x8XY0(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10
    chip8.V[chip8.y] = 0x20
    
    chip8.set_X_to_Y() # Run opcode
    if chip8.V[chip8.x] != chip8.V[chip8.y]:
        return 0
    return 1
    
# 0x8XY1 - set_register_OR()
def test_0x8XY1(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x05 # 0101
    chip8.V[chip8.y] = 0x02 # 0010
    
    chip8.set_register_OR()
    if chip8.V[chip8.x] != 0x07:
        return 0
    return 1

# 0x8XY2 - set_register_AND()
def test_0x8XY2(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x05 # 0101
    chip8.V[chip8.y] = 0x03 # 0011
    
    chip8.set_register_AND()
    if chip8.V[chip8.x] != 0x01:
        return 0
    return 1    

# 0x8XY3 - set_register_XOR()
def test_0x8XY3(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x05 # 0101
    chip8.V[chip8.y] = 0x03 # 0011
    
    chip8.set_register_XOR()
    if chip8.V[chip8.x] != 0x06:
        return 0
    return 1 

# 0x8XY4 - add_registers()
# No carry case
def test_0x8XY4_nocarry(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10 # 0101
    chip8.V[chip8.y] = 0x20 # 0011
    
    chip8.add_registers()
    if chip8.V[chip8.x] != 0x30 or chip8.V[0xF] != 0:
        return 0
    return 1 

# 0x8XY4 - add_registers()
# Carry case
def test_0x8XY4_carry(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0xFF # 0101
    chip8.V[chip8.y] = 0x01 # 0011
    
    chip8.add_registers()
    if chip8.V[chip8.x] != 0x0 or chip8.V[0xF] != 1:
        return 0
    return 1 
    
# 0x8XY5 - subtract_registers()
# No borrow case
def test_0x8XY5_noborrow(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x20
    chip8.V[chip8.y] = 0x10 
    
    
    chip8.subtract_registers()
    if chip8.V[chip8.x] != 0x10 or chip8.V[0xF] != 1:
        return 0
    return 1 

# 0x8XY5 - subtract_registers()
# Borrow case
def test_0x8XY5_borrow(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x20
    chip8.V[chip8.y] = 0x30
    
    chip8.subtract_registers()
    if chip8.V[chip8.x] != 0xF0 or chip8.V[0xF] != 0:
        return 0
    return 1 

# 0x8XY6 - shift_right()
def test_0x8XY6(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.y] = 0x05 # 0101
    
    chip8.shift_right()
    if chip8.V[0xF] != 1 or chip8.V[chip8.x] != 0x02:
        return 0
    return 1

# 0x8XY7 - subtract_registers_reversed()
# No borrow case
def test_0x8XY7_noborrow(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x20
    chip8.V[chip8.y] = 0x30
    
    chip8.subtract_registers_reversed()
    if chip8.V[chip8.x] != 0x10 or chip8.V[0xF] != 1:
        return 0
    return 1

# 0x8XY7 - subtract_registers_reversed()
# Borrow case
def test_0x8XY7_borrow(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x30
    chip8.V[chip8.y] = 0x20
    
    chip8.subtract_registers_reversed()
    if chip8.V[chip8.x] != 0xF0 or chip8.V[0xF] != 0:
        return 0
    return 1

# 0x8XYE - shift_left()
def test_0x8XYE(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.y] = 0x11 # 0001 0001
    
    chip8.shift_left()
    if chip8.V[0xF] != 0xA & 0x80 or chip8.V[chip8.x] != 0x22:
        return 0
    return 1
    
# 0x9XY0 - skip_if_registers_unequal()
# Unequal case
def test_0x9XY0_unequal(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10
    chip8.V[chip8.y] = 0x20
    
    chip8.skip_if_registers_unequal() # Run opcode
    if chip8.program_counter != 0x204: # If pc is not incremented by 2
        return 0 # Return false
    return 1
    
# 0x9XY0 - skip_if_registers_unequal()
# Equal case
def test_0x9XY0_equal(chip8):
    chip8.initialize() # Reset values
    chip8.x = 0x1 # Set x
    chip8.y = 0x2 # Set y
    chip8.V[chip8.x] = 0x10
    chip8.V[chip8.y] = 0x10
    
    chip8.skip_if_registers_unequal() # Run opcode
    if chip8.program_counter != 0x202: # If pc is not incremented by 2
        return 0 # Return false
    return 1
    
# 0xANNN - set_I()
def test_0xANNN(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0xA121
    
    chip8.set_I()
    if chip8.I != chip8.operation_code & 0x0FFF:
        return 0
    return 1        

# 0xBNNN - jump_first_register()    
def test_0xBNNN(chip8):
    chip8.initialize() # Reset values
    chip8.operation_code = 0xBEEF
    chip8.V[0] = 0x0014
    
    chip8.jump_first_register()
    
    if chip8.program_counter != 0x0EEF + 0x0014:
        return 0
    return 1

# 0xCXNN - set_register_random()
def test_0xCXNN(chip8):
    chip8.initialize() # Reset values
    chip8.set_register_random()
    print(hex(chip8.V[chip8.x]))

# 0xDXYN - draw_to_screen()
def test_0xDXYN(chip8):
    chip8.initialize()
    chip8.operation_code = 0xD121
    chip8.x = 1
    chip8.y = 2
    chip8.V[1] = 0
    chip8.V[2] = 4
    chip8.I = 0
    
    chip8.memory[chip8.I] = 0b10011001
    
    chip8.draw_to_screen()
    
    if (chip8.screen_pixel_states[256] != 1) or (chip8.screen_pixel_states[257] != 0) or (chip8.screen_pixel_states[258] != 0) or (chip8.screen_pixel_states[259] != 1) or (chip8.screen_pixel_states[260] != 1) or (chip8.screen_pixel_states[261] != 0) or (chip8.screen_pixel_states[262] != 0) or (chip8.screen_pixel_states[263] != 1):
        return 0
    return 1

# 0xEX9E - skip_if_key_press()
def test_0xEX9E(chip8):
    chip8.initialize()
    chip8.operation_code = 0xE19E
    chip8.x = 1
    chip8.keys[chip8.V[chip8.x]] = 1

    chip8.skip_if_key_press()
    if chip8.program_counter != 0x204:
        return 0
    return 1
        
# 0xEXA1 - skip_if_no_key_press()
def test_0xEXA1(chip8):
    chip8.initialize()
    chip8.operation_code = 0xE1A1
    chip8.x = 1
    chip8.keys[chip8.V[chip8.x]] = 0

    chip8.skip_if_no_key_press()
    if chip8.program_counter != 0x204:
        return 0
    return 1

# 0xFX07 - set_register_to_delay()
def test_0xFX07(chip8):
    chip8.initialize()
    chip8.x = 1
    chip8.delay_timer = 10
    chip8.set_register_to_delay()
    
    if chip8.V[chip8.x] != chip8.delay_timer:
        return 0
    return 1
    
# 0xFX0A - wait_for_key_press()
def test_0xFX0A(chip8):
    chip8.initialize()
    chip8.keys[3] = 1
    chip8.wait_for_key_press()
    if chip8.V[chip8.x] != 3:
        return 0
    return 1
    
# 0xFX15 - set_delay_timer()
def test_0xFX15(chip8):
    chip8.initialize()
    chip8.x = 1
    chip8.V[chip8.x] = 88
    chip8.set_delay_timer()
    
    if chip8.delay_timer != chip8.V[chip8.x]:
        return 0
    return 1
    
# 0xFX18 - set_sound_timer()
def test_0xFX18(chip8):
    chip8.initialize()
    chip8.x = 1
    chip8.V[chip8.x] = 88
    chip8.set_sound_timer()
    
    if chip8.sound_timer != chip8.V[chip8.x]:
        return 0
    return 1
    
# 0xFX1E - add_I()
def test_0xFX1E(chip8):
    chip8.initialize
    chip8.x = 1
    chip8.V[chip8.x] = 20
    old_I = chip8.I
    chip8.add_I()
    
    if old_I != (chip8.I - chip8.V[chip8.x]):
        return 0
    return 1

# 0xFX29 - set_I_to_address()
def test_0xFX29(chip8):
    chip8.initialize
    chip8.x = 1
    chip8.V[chip8.x] = 3
    chip8.set_I_to_address()
    
    if chip8.I != 15:
        return 0
    return 1
    
# 0xFX33 - convert_to_binary()
def test_0xFX33(chip8):
    chip8.initialize
    chip8.x = 1
    chip8.V[chip8.x] = 369
    chip8.convert_to_binary()
    
    if chip8.memory[chip8.I] != 3 or chip8.memory[chip8.I + 1] != 6 or chip8.memory[chip8.I + 2] != 9:
        return 0
    return 1
    
# 0xFX55 - store_registers_in_memory()
def test_0xFX55(chip8):
    chip8.initialize
    chip8.x = 5
    chip8.V[0] = 0
    chip8.V[1] = 1
    chip8.V[2] = 2
    chip8.V[3] = 3
    chip8.V[4] = 4
    chip8.V[chip8.x] = 5

    old_I = chip8.I
    chip8.store_registers_in_memory()
    
    if chip8.memory[old_I] != 0 or chip8.memory[old_I + 1] != 1 or chip8.memory[old_I + 2] != 2 or chip8.memory[old_I + 3] != 3 or chip8.memory[old_I + 4] != 4 or chip8.memory[old_I + 5] != 5 or chip8.I != old_I + 6:
        return 0
    return 1
    
# 0xFX65 - fill_registers()
def test_0xFX65(chip8):
    chip8.initialize
    chip8.memory[chip8.I] = 0
    chip8.memory[chip8.I + 1] = 1
    chip8.memory[chip8.I + 2] = 2
    chip8.memory[chip8.I + 3] = 3
    chip8.memory[chip8.I + 4] = 4
    chip8.memory[chip8.I + 5] = 5
    chip8.x = 5
    old_I = chip8.I
    
    chip8.fill_registers()
    
    if chip8.V[0] != 0 or chip8.V[1] != 1 or chip8.V[2] != 2 or chip8.V[3] != 3 or chip8.V[4] != 4 or chip8.V[5] != 5 or chip8.I != old_I + 6:
        return 0
    return 1
    

def main():
    CHIP8 = mychip8.MyChip8()
    assert (test_0x00E0(CHIP8)), "0x00E0, clear_screen() Error"
    assert (test_0x00EE(CHIP8)), "0x00EE, return_address() Error"
    assert (test_0x1NNN(CHIP8)), "0x1NNN, jump_address() Error"
    assert (test_0x2NNN(CHIP8)), "0x2NNN, call_subroutine() Error"
    assert (test_0x3XNN_unequal(CHIP8)), "0x3XNN, skip_if_equal() Error, Unequal Case"
    assert (test_0x3XNN_equal(CHIP8)), "0x3XNN, skip_if_equal() Error, Equal Case"
    assert (test_0x4XNN_unequal(CHIP8)), "0x4XNN, skip_if_unequal() Error, Unequal Case"
    assert (test_0x4XNN_equal(CHIP8)), "0x4XNN, skip_if_unequal() Error, Equal Case"
    assert (test_0x5NNN_unequal(CHIP8)), "0x5NNN, skip_if_registers_equal() Error, Unequal Case"
    assert (test_0x5NNN_equal(CHIP8)), "0x5NNN, skip_if_registers_equal() Error, Equal Case"
    assert (test_0x6XNN(CHIP8)), "0x6XNN, set_register_value() Error"
    assert (test_0x7XNN(CHIP8)), "0x7XNN, register_add_value() Error"
    assert (test_0x8XY0(CHIP8)), "0x8XY0, set_X_to_Y() Error"
    assert (test_0x8XY1(CHIP8)), "0x8XY1, set_register_OR() Error"
    assert (test_0x8XY2(CHIP8)), "0x8XY2, set_register_AND() Error"
    assert (test_0x8XY3(CHIP8)), "0x8XY3, set_register_XOR() Error"
    assert (test_0x8XY4_nocarry(CHIP8)), "0x8XY4, add_registers() Error, No Carry Case"
    assert (test_0x8XY4_carry(CHIP8)), "0x8XY4, add_registers() Error, Carry Case"
    assert (test_0x8XY5_noborrow(CHIP8)), "0x8XY5, subtract_registers() Error, No Borrow Case"
    assert (test_0x8XY5_borrow(CHIP8)), "0x8XY5, subtract_registers() Error, Borrow Case"
    assert (test_0x8XY6(CHIP8)), "0x8XY6, shift_right() Error"
    assert (test_0x8XY7_noborrow(CHIP8)), "0x8XY7, subtract_registers_reversed() Error, No Borrow Case"
    assert (test_0x8XY7_borrow(CHIP8)), "0x8XY7, subtract_registers_reversed() Error, Borrow Case"
    assert (test_0x8XYE(CHIP8)), "0x8XYE, shift_left() Error"
    assert (test_0x9XY0_unequal(CHIP8)), "0x9XY0, skip_if_registers_unequal() Error, Unequal Case"
    assert (test_0x9XY0_equal(CHIP8)), "0x9XY0, skip_if_registers_unequal() Error, Equal Case"
    assert (test_0xANNN(CHIP8)), "0xANNN, set_I() Error"
    assert (test_0xBNNN(CHIP8)), "0xBNNN, jump_first_register() Error"
    test_0xCXNN(CHIP8)
    assert (test_0xDXYN(CHIP8)), "0xDXYN, draw_to_screen() Error"
    assert (test_0xEX9E(CHIP8)), "0xEX9E, skip_if_key_press() Error"
    assert (test_0xEXA1(CHIP8)), "0xEXA1, skip_if_no_key_press() Error"
    assert (test_0xFX07(CHIP8)), "0xFX07, set_register_to_delay() Error"
    assert (test_0xFX0A(CHIP8)), "0xFX0A, wait_for_key_press() Error"
    assert (test_0xFX15(CHIP8)), "0xFX15, set_delay_timer() Error"
    assert (test_0xFX18(CHIP8)), "0xFX18, set_delay_timer() Error"
    assert (test_0xFX1E(CHIP8)), "0xFX1E, add_I() Error"
    assert (test_0xFX29(CHIP8)), "0xFX29, set_I_to_address() Error"
    assert (test_0xFX33(CHIP8)), "0xFX33, convert_to_binary() Error"
    assert (test_0xFX55(CHIP8)), "0xFX55, store_registers_in_memory() Error"
    assert (test_0xFX65(CHIP8)), "0xFX65, fill_registers() Error"
    
if __name__ == "__main__":
    main()