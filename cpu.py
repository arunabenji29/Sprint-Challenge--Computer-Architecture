import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0b11110100
        self.fl = [0] * 8

    def ram_read(self,address):
        MAR = address
        return self.ram[address]

    def ram_write(self,address,value):
        MDR = value
        self.ram[address] = value

    def load(self,filename):
        """Load a program into memory."""

        try:

            address = 0

            with open(filename) as f:
                for line in f:
                    hash_split = line.split("#")
                    binary_code = hash_split[0].strip()
                    try:
                        if binary_code is not None:
                            val = int(binary_code)
                    except ValueError:
                        continue
                    self.ram_write(address,val)
                    address += 1
                # print(f'copied {self.ram}')

        except FileNotFoundError:
            print(f"{sys.argv[0]} : {sys.argv[1]} not found")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # IR  = self.pc
        # operand_a = self.ram_read(self.pc+1)
        # operand_b = self.ram_read(self.pc+2)

        running = True
        # curr_addr = 0

        LDI = 0b10000010
        CMP = 0b10100111
        JEQ = 0b01010101
        PRN = 0b01000111
        JNE = 0b01010110
        JMP = 0b01010100
        HLT = 0b00000001

        while running:
            # print('running')
            IR  = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            

            if int(f"0b{IR}",2) == LDI:
                # print('\nLDI')
                self.reg[int(f'{operand_a}',2)] = int(f'{operand_b}',2)
                # print(f"load: register{int(f'{self.ram_read(self.pc+1)}',2)} value:{self.reg[int(f'{self.ram_read(self.pc+1)}',2)]}")
                
                shift = int(f'{IR}',2)
                incr = shift >> 6
                self.pc += (incr + 1)
                
            elif int(f"0b{IR}",2) == CMP:
                # print('\nCMP')
                # print(f'reg a: value - {self.reg[int(f"{operand_a}",2)]}')
                # print(f'reg b: value - {self.reg[int(f"{operand_b}",2)]}')
                # self.reg[operand_a] = operand_b

                if self.reg[int(f"{operand_a}",2)] < self.reg[int(f"{operand_b}",2)]:
                    self.fl[5] = 1
                elif self.reg[int(f"{operand_a}",2)] > self.reg[int(f"{operand_b}",2)]:
                    self.fl[6] = 1
                elif self.reg[int(f"{operand_a}",2)] == self.reg[int(f"{operand_b}",2)]:
                    self.fl[7] = 1
                # print(f'flag {self.fl}')
                shift = int(f'{IR}',2)
                incr = shift >> 6
                self.pc += (incr + 1)
                

            elif int(f"0b{IR}",2) == JEQ:
                # print('\nJEQ')

                if self.fl[7] == 1:

                    self.pc = self.reg[int(f'{operand_a}',2)]

                    # print(f'address jump: {self.pc}')

                else:
                    shift = int(f'{IR}',2)
                    incr = shift >> 6
                    self.pc += (incr + 1) 

                

            elif int(f"0b{IR}",2) == PRN:
                print(f'print: {self.reg[int(f"{operand_a}",2)]}')

                shift = int(f'{IR}',2)
                incr = shift >> 6
                self.pc += (incr + 1)

           
            elif int(f"0b{IR}",2) == JNE:
                # print('\nJNE')

                if self.fl[7] == 0:

                    self.pc = self.reg[int(f'{operand_a}',2)]

                    # print(f'address jump: {self.pc}')

                else:
                    shift = int(f'{IR}',2)
                    incr = shift >> 6
                    self.pc += (incr + 1)


            elif int(f"0b{IR}",2) == JMP:
                # print('\nJMP')

                self.pc = self.reg[int(f'{operand_a}',2)]

                

            elif int(f"0b{IR}",2) == HLT:
                # print('\nHLT')

                sys.exit(1)
