# http://mattmik.com/files/chip8/mastering/chip8.html
# http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
import sys
import random
from time import time

class MyChip8:
    def initialize(self):
        # Font sprite data stored in the first 80 bytes of memory
        self.memory = [0xF0, 0x90, 0x90, 0x90, 0xF0, # 1
        0x20, 0x60, 0x20, 0x20, 0x70, # 2
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 3
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 4
        0x90, 0x90, 0xF0, 0x10, 0x10, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80] # F 
        self.memory.extend([0x00] * 0xFB0) # Extend memory by 4016 for a total of 4096 bytes
        self.V = [0] * 16 # Initialize 16 registers
        self.I = 0 # Index register
        self.stack_pointer = 0
        self.memory = [0] * 4096
        self.program_counter = 0x200 # Program counter starts at 0x200 since first 200 bytes are unused
        self.opcode = 0
        self.stack = []
        self.screen_pixel_states = [0] * 2048 # Initialize 2048 pixels (64 x 32 screen) with states 1 (white) or 0 (black)
        self.should_draw = True # If flag is True, update screen
        self.keys = [0] * 16 # Initialize key registers
        self.delay_timer = 0
        self.sound_timer = 0
        self.last_timer_value = time() # Initialize starting time
    
    def load_game_rom(self, file_name):
        with open(file_name, 'rb') as game_rom:
            byte = game_rom.read()
            for bit in range(len(byte)):
                self.memory[self.program_counter + bit] = byte[bit]
    # ----------------------------------------------------------------------------
    # ============================= OPERATION CODES ==============================
    # ----------------------------------------------------------------------------
    # Each instruction is 2 bytes long so the program counter should be incremented by 2 every time an opcode is executed.
    # The program counter SHOULD NOT be incremented if opcode calls for a jump to a certain address in memory or calls for a subroutine.
    # If an opcode is to be skipped, increment program counter by 4.
    
    # 0x00E0 - Clear the screen
    def clear_screen(self):
        for pixel in range(len(self.screen_pixel_states)): # Set each pixel to state 0 (black)
            self.screen_pixel_states[pixel] = 0;
        self.should_draw = True
        self.program_counter += 2
    
    # 0x00EE - Return from subroutine -> load address from stack
    def return_address(self):
        self.program_counter = self.stack.pop()
    
    # 0x1NNN - Jump to address NNN
    def jump_address(self):
        self.program_counter = self.operation_code & 0x0FFF # Get NNN
        
    # 0x2NNN - Execute subroutine starting at address NNN
    def call_subroutine(self):
        self.program_counter += 2
        self.stack.append(self.program_counter)
        self.program_counter = self.operation_code & 0x0FFF # Get NNN     
    
    # 0x3NNN - Skip the following instruction if the value of register VX equals NN
    def skip_if_equal(self):
        if self.V[self.x] == self.operation_code & 0x00FF: # Compare V[x] with NN
            self.program_counter += 4 # Skip opcode, increment by 4 instead of 2
        else:
            self.program_counter += 2
    
    # 0x4NNN - Skip the following instruction if the value of register VX is not equal NN
    def skip_if_unequal(self):
        if self.V[self.x] != self.operation_code & 0x00FF: # Compare V[x] with NN
            self.program_counter += 4 # Skip opcode, increment by 4 instead of 2
        else:
            self.program_counter += 2
    
    # 0x5NNN - Skip the following instruction if the value of register VX is equal to the value of register VY
    def skip_if_registers_equal(self):
        if self.V[self.x] == self.V[self.y]:
            self.program_counter += 4 # Skip opcode, increment by 4 instead of 2
        else:
            self.program_counter += 2
    
    # 0x6XNN - Store number NN in register VX
    def set_register_value(self):
        self.V[self.x] = self.operation_code & 0x00FF # Get NN
        self.program_counter += 2 # Increment by 2
    
    # 0x7XNN - Add number NN to register VX
    def register_add_value(self):
        self.V[self.x] += self.operation_code & 0x00FF # Get NN
        self.program_counter += 2 # Increment by 2
        
    # 8XY0 - Store the value of register VY in register VX
    def set_X_to_Y(self):
        self.V[self.x] = self.V[self.y]
        self.program_counter += 2 # Increment by 2
    
    # 8XY1 - Set VX to VX OR VY
    def set_register_OR(self):
        self.V[self.x] = self.V[self.x] | self.V[self.y] 
        self.program_counter += 2 # Increment by 2
    
    # 8XY2 - Set VX to VX AND VY
    def set_register_AND(self):
        self.V[self.x] = self.V[self.x] & self.V[self.y] 
        self.program_counter += 2 # Increment by 2
    
    # 8XY3 - Set VX to VX XOR VY
    def set_register_XOR(self):
        self.V[self.x] = self.V[self.x] ^ self.V[self.y] 
        self.program_counter += 2 # Increment by 2
        
    # 8XY4 - Add the value of register VY to register VX 
    # Set VF to 01 if a carry occurs
    # Set VF to 00 if a carry does not occur
    def add_registers(self):
        self.V[self.x] += self.V[self.y] 
        if self.V[self.x] > 0xFF:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0
        self.V[self.x] &= 0xFF
        self.program_counter += 2 # Increment by 2
        
    # 8XY5 - Subtract the value of register VY from register VX
    # Set VF to 00 if a borrow occurs
    # Set VF to 01 if a borrow does not occur
    def subtract_registers(self):
        if self.V[self.x] < self.V[self.y]:
            self.V[0xF] = 0
        else:
            self.V[0xF] = 1
        self.V[self.x] -= self.V[self.y] 
        self.V[self.x] &= 0xFF
        self.program_counter += 2 # Increment by 2
    
    # 8XY6 - Store the value of register VY shifted right one bit in register VX
    # Set register VF to the least significant bit prior to the shift
    def shift_right(self):
        self.V[0xF] = self.V[self.y] & 0x01
        self.V[self.x] = self.V[self.y] >> 1
        self.program_counter += 2 # Increment by 2
        
    # 8XY7 - Set register VX to the value of VY minus VX
    # Set VF to 00 if a borrow occurs
    # Set VF to 01 if a borrow does not occur
    def subtract_registers_reversed(self):
        if self.V[self.y] < self.V[self.x]:
            self.V[0xF] = 0
        else:
            self.V[0xF] = 1
        self.V[self.x] = self.V[self.y] - self.V[self.x]
        self.V[self.x] &= 0xFF
        self.program_counter += 2 # Increment by 2
    
    # 8XYE - Store the value of register VY shifted left one bit in register VX
    # Set register VF to the most significant bit prior to the shift
    def shift_left(self):
        self.V[0xF] = self.V[self.y] & 0x80
        self.V[self.x] = self.V[self.y] << 1
        self.program_counter += 2 # Increment by 2
    
    # 0x9XY0 - Skip the following instruction if the value of register VX is not equal to the value of register VY
    def skip_if_registers_unequal(self):
        if self.V[self.x] != self.V[self.y]:
            self.program_counter += 4  # Skip opcode, increment by 4 instead of 2
        else:
            self.program_counter += 2
    
    # 0xANNN - Store memory address NNN in register I
    def set_I(self):
        self.I = self.operation_code & 0x0FFF
        self.program_counter += 2 # Increment by 2
        
    # 0xBNNN - Jump to address NNN + V0
    def jump_first_register(self):
        self.program_counter = self.operation_code & 0x0FFF + self.V[0]
    
    # 0xCXNN - Set VX to a random number with a mask of NN
    def set_register_random(self):
        random_number = random.randrange(256)
        self.V[self.x] = random_number & (self.operation_code & 0x00FF)
        self.program_counter += 2 
    
    # 0xDXYN - Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
    # Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
    def draw_to_screen(self):
        height = self.operation_code & 0x000F
        x_coord = self.V[self.x]
        y_coord = self.V[self.y]
        self.V[0xF] = 0 # If pixel on display is set to 1, collision is registered by setting VF
        
        for y in range(height): # Loop over each row
            pixel = self.memory[self.I + y] # Fetch pixel value at memory location
            for x in range(8): # Width of each sprite fixed to 8 bits
                if (pixel & (0x80 >> x)) != 0 and not (x + x_coord >= 64 or y + y_coord >= 32): # Scan through each bit
                    if self.screen_pixel_states[x_coord + x + ((y_coord + y) * 64)] == 1: # Check if current pixel is set to 1
                        self.V[0xF] = 1
                    self.screen_pixel_states[x_coord + x + ((y_coord + y) * 64)] ^= 1 # Set pixel value using XOR
        self.should_draw = True
        self.program_counter += 2
                    
    # 0xEX9E - Skip the following instruction if the key corresponding to the hex value currently stored in register VX is pressed
    def skip_if_key_press(self):
        if self.keys[self.V[self.x]] == 1:
            self.program_counter += 4
        else:
            self.program_counter += 2
    
    # 0xEXA1 - Skip the following instruction if the key corresponding to the hex value currently stored in register VX is not pressed
    def skip_if_no_key_press(self):
        if self.keys[self.V[self.x]] == 0:
            self.program_counter += 4
        else:
            self.program_counter += 2
        
    # FX07 - Store the current value of the delay timer in register VX
    def set_register_to_delay(self):
        self.V[self.x] = self.delay_timer
        self.program_counter += 2
        
    # FX0A - Wait for a keypress and store the result in register VX    
    def wait_for_key_press(self):
        key_press = -1
        for key in range(len(self.keys)): # Iterate through key registers
            if self.keys[key] == 1: # If register is in pressed state
                key_press = key
                break
        if key_press > 0: # If a key register is pressed
            self.V[self.x] = key_press
        else:
            self.program_counter -= 2
        self.program_counter += 2
    
    # FX15 - Set the delay timer to the value of register VX
    def set_delay_timer(self):
        self.delay_timer = self.V[self.x]
        self.program_counter += 2
        
    # FX18 - Set the sound timer to the value of register VX
    def set_sound_timer(self):
        self.sound_timer = self.V[self.x]
        self.program_counter += 2
    
    # FX1E - Add the value stored in register VX to register I
    def add_I(self):
        self.I += self.V[self.x]
        self.program_counter += 2
    
    # FX29 - Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register VX
    def set_I_to_address(self):
        self.I = self.V[self.x] * 5 # 5 values for each character
        self.program_counter += 2
    
    # FX33 - Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2
    def convert_to_binary(self):
        self.memory[self.I] = self.V[self.x] // 100 # MSB
        self.memory[self.I + 1] = (self.V[self.x] % 100) // 10 
        self.memory[self.I + 2] = self.V[self.x] % 10 # LSB 
        self.program_counter += 2
    
    # FX55 - Store the values of registers V0 to VX inclusive in memory starting at address I
    # I is set to I + X + 1 after operation
    def store_registers_in_memory(self):
        for register in range(self.x + 1):
            self.memory[self.I + register] = self.V[register]
        self.I += self.x + 1
        self.program_counter += 2
    
    # FX65 - Fill registers V0 to VX inclusive with the values stored in memory starting at address I
    # I is set to I + X + 1 after operation
    def fill_registers(self):
        for register in range(self.x + 1):
            self.V[register] = self.memory[self.I + register]
        self.I += self.x + 1
        self.program_counter += 2
            
        
    # ----------------------------------------------------------------------------
    # =========================== END OPERATION CODES ============================
    # ----------------------------------------------------------------------------
    
    def emulate_cycle(self):
        # Fetch opcode
        self.operation_code = self.memory[self.program_counter] << 8 | self.memory[self.program_counter + 1]
        print(hex(self.operation_code))
        # Sprite positions
        self.x = (self.opcode & 0x0F00) >> 8
        self.y = (self.opcode & 0x00F0) >> 4
        
        # 0x0___ opcodes
        if (self.operation_code & 0xF000 == 0x0000):
            # 00E0 - Clear the screen
            if (self.operation_code == 0x00E0):
                self.clear_screen()
            # 00EE - Return from subroutine -> load address from stack
            elif (self.operation_code == 0x00EE):
                self.return_address()
        # 0x1NNN - Jump to address NNN
        elif (self.operation_code & 0xF000 == 0x1000):
            self.jump_address()
        # 0x2NNN - Execute subroutine starting at address NNN
        elif (self.operation_code & 0xF000 == 0x2000):
            self.call_subroutine()
        # 0x3XNN - Skip the following instruction if the value of register VX equals NN
        elif (self.operation_code & 0xF000 == 0x3000):
            self.skip_if_equal()
        # 0x4XNN - Skip the following instruction if the value of register VX is not equal to NN
        elif (self.operation_code & 0xF000 == 0x4000):
            self.skip_if_unequal()
        # 0x5XY0 - Skip the following instruction if the value of register VX is equal to the value of register VY
        elif (self.operation_code & 0xF000 == 0x5000):
            self.skip_if_registers_equal()
        # 0x6XNN - Store number NN in register VX
        elif (self.operation_code & 0xF000 == 0x6000):
            self.set_register_value()
        # 0x7XNN - Add the number NN to register VX
        elif (self.operation_code & 0xF000 == 0x7000):
            self.register_add_value()
        # 0x8___ opcodes
        elif (self.operation_code & 0xF000 == 0x8000):
            # 8XY0 - Store the value of register VY in register VX
            if (self.operation_code & 0x000F == 0x0000):
                self.set_X_to_Y()
            # 8XY1 - Set VX to VX OR VY
            elif (self.operation_code & 0x000F == 0x0001):
                self.set_register_OR()
            # 8XY2 - Set VX to VX AND VY
            elif (self.operation_code & 0x000F == 0x0002):
                self.set_register_AND()
            # 8XY3 - Set VX to VX XOR VY
            elif (self.operation_code & 0x000F == 0x0003):
                self.set_register_XOR()
            # 8XY4 - Add the value of register VY to register VX 
            # Set VF to 01 if a carry occurs
            # Set VF to 00 if a carry does not occur
            elif (self.operation_code & 0x000F == 0x0004):
                self.add_registers()
            # 8XY5 - Subtract the value of register VY from register VX
            # Set VF to 00 if a borrow occurs
            # Set VF to 01 if a borrow does not occur
            elif (self.operation_code & 0x000F == 0x0005):
                self.subtract_registers()
            # 8XY6 - Store the value of register VY shifted right one bit in register VX
            # Set register VF to the least significant bit prior to the shift
            elif (self.operation_code & 0x000F == 0x0006):
                self.shift_right()
            # 8XY7 - Set register VX to the value of VY minus VX
            # Set VF to 00 if a borrow occurs
            # Set VF to 01 if a borrow does not occur
            elif (self.operation_code & 0x000F == 0x0007):
                self.subtract_registers_reversed()
            # 8XYE - Store the value of register VY shifted left one bit in register VX
            # Set register VF to the most significant bit prior to the shift
            elif (self.operation_code & 0x000F == 0x000E):
                self.shift_left()
        # 0x9XY0 - Skip the following instruction if the value of register VX is not equal to the value of register VY
        elif (self.operation_code & 0xF000 == 0x9000):
            self.skip_if_registers_unequal()
        # 0xANNN - Store memory address NNN in register I
        elif (self.operation_code & 0xF000 == 0xA000):
            self.set_I()
        # 0xBNNN - Jump to address NNN + V0
        elif (self.operation_code & 0xF000 == 0xB000):
            self.jump_first_register()
        # 0xCXNN - Set VX to a random number with a mask of NN
        elif (self.operation_code & 0xF000 == 0xC000):
            self.set_register_random()
        # 0xDXYN - Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I
        # Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
        elif (self.operation_code & 0xF000 == 0xD000):
            self.draw_to_screen()
        # 0xE___ opcodes
        elif (self.operation_code & 0xF000 == 0xE000):
            # EX9E - Skip the following instruction if the key corresponding to the hex value currently stored in register VX is pressed
            if (self.operation_code & 0x00FF == 0x009E):
                self.skip_if_key_press()
            # EXA1 - Skip the following instruction if the key corresponding to the hex value currently stored in register VX is not pressed
            elif (self.operation_code & 0x00FF == 0x00A1):
                self.skip_if_no_key_press()
        # 0xF___ opcodes
        elif (self.operation_code & 0xF000 == 0xF000):
            # FX07 - Store the current value of the delay timer in register VX
            if (self.operation_code & 0x00FF == 0x0007):
                self.set_register_to_delay()
            # FX0A - Wait for a keypress and store the result in register VX
            elif (self.operation_code & 0x00FF == 0x000A):
                self.wait_for_key_press()          
            # FX15 - Set the delay timer to the value of register VX
            elif (self.operation_code & 0x00FF == 0x0015):   
                self.set_delay_timer()
            # FX18 - Set the sound timer to the value of register VX
            elif (self.operation_code & 0x00FF == 0x0018): 
                self.set_sound_timer()
            # FX1E - Add the value stored in register VX to register I
            elif (self.operation_code & 0x00FF == 0x001E):
                self.add_I()
            # FX29 - Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register VX
            elif (self.operation_code & 0x00FF == 0x0029):
                self.set_I_to_address()
            # FX33 - Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2
            elif (self.operation_code & 0x00FF == 0x0033):
                self.convert_to_binary()
            # FX55 - Store the values of registers V0 to VX inclusive in memory starting at address I
            #I is set to I + X + 1 after operation
            elif (self.operation_code & 0x00FF == 0x0055):
                self.store_registers_in_memory()
            # FX65 - Fill registers V0 to VX inclusive with the values stored in memory starting at address I
            # I is set to I + X + 1 after operation
            elif (self.operation_code & 0x00FF == 0x0065):
                self.fill_registers()
        # Handle unknown opcode
        else:
            print("Unknown instruction:" + hex(self.operation_code))
            self.program_counter += 2
        
        current_timer_value = time() # Get integer of current time
        if current_timer_value - self.last_timer_value >= 1.0/60: # If at least 1/60th of a second has passed
            if self.delay_timer > 0: 
                self.delay_timer -= 1 # Decrement delay timer
	
            if self.sound_timer > 0:
                self.sound_timer -= 1 # Decrement sound timer
			
            self.last_timer_value = current_timer_value # Set the last time value recorded to current time value  
        

if __name__ == "__main__":
    from main import mainloop
    mainloop()
    
        
        