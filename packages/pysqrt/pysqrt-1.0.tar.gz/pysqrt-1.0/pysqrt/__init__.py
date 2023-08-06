#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class sqrt:
    def __init__(self, number, max):
        """
        Documentation of the algorithm
        can be found here: https://en.wikipedia.org/wiki/Shifting_nth_root_algorithm
        """
        self.max = max                          # set maximal size after the comma
        self.number = self.getpacks(number)
        self.cache = [None, None, None, None]   # to manage steps


    def getSqrt(self):
        """look at the Docs of wikipedia"""
        self.cache[0] = str(self.getNearest(int(self.number[0])))
        self.cache[1] = str(int(self.number[0]) - int(self.cache[0]) ** 2)
        for x in self.number[1:]:
            if x != ".":
                self.cache[1] += x
                if int(int(self.cache[1][:-1]) / (int(self.cache[0]) * 2)) > 9:
                    self.cache[3] = 9
                else:
                    self.cache[3] = int(int(self.cache[1][:-1]) / (int(self.cache[0]) * 2))

                self.cache[2] = int(str(int(self.cache[0]) * 2) + str(self.cache[3]))

                while self.cache[2] * self.cache[3] > int(self.cache[1]):
                    self.cache[2] -= 1
                    self.cache[3] -= 1


                self.cache[0] += str(self.cache[3])
                self.cache[1] = str(int(self.cache[1]) - (self.cache[2] * self.cache[3]))

        if "." in self.number:
            self.cache[0] = self.cache[0][:self.number.index(".")] + "." + self.cache[0][self.number.index("."):]

        return self.cache[0]



    def getNearest(self, number):
        """get the nearest square root"""
        for x in range(number + 2):
            if x**2 > number:
                return x - 1

    def getpacks(self, number):
        """get packs of two numbers"""
        output = []
        if "." in str(number):
            for x in range(len(str(number).split(".")[0]) - 1, 0, -2):
                output.insert(0, str(number).split(".")[0][x - 1: x + 1])

            if len(str(number).split(".")[0]) % 2 != 0:
                output.insert(0, str(number)[0])

            output.append(".")

            for x in range(0, len(str(number).split(".")[1]) - 1, 2):
                output.append(str(number).split(".")[1][x: x + 2])


            if len(str(number).split(".")[1]) % 2 != 0:
                output.append(str(number)[-1])

            if len(number) < self.max:
                for x in range(len(number) - self.max):
                    self.output.append("00")

        else:
            for x in range(len(str(number)) - 1, 0, -2):
                output.insert(0, str(number)[x - 1: x + 1])

            if len(str(number)) % 2 != 0:
                output.insert(0, str(number)[0])

            if self.max:
                output.append(".")
                for x in range(self.max):
                    output.append("00")


        return output


def main():
    s = sqrt(2, 10000)
    print(s.getSqrt())

if __name__ == '__main__':
    main()
