import numpy as np
import random
import sys


class Enigma():
    def __init__(self, plane, alphabet, plug_perm, ref_perm):
        self.alphabet = alphabet
        self.char_dict = {x: n for n, x in enumerate(alphabet)}
        self.size = len(alphabet)
        self.identity = np.eye(self.size)
        self.plug_perm = plug_perm
        self.ref_perm = ref_perm
        self.rot1_perm = random.sample(range(self.size), self.size)
        self.rot2_perm = random.sample(range(self.size), self.size)
        self.rot3_perm = random.sample(range(self.size), self.size)
        self.plane = plane

    def get_matrix(self, cnt1, cnt2, cnt3):
        rot_rotor_perm = list(range(self.size))

        col_perm_mat = np.mat([self.identity[n - 1] for n in rot_rotor_perm])
        row_perm_mat = col_perm_mat.T

        plugbord = np.mat([self.identity[n] for n in self.plug_perm])
        reflector = np.mat([self.identity[n] for n in self.ref_perm])
        rotor1 = np.mat([self.identity[n] for n in self.rot1_perm])
        rotor2 = np.mat([self.identity[n] for n in self.rot2_perm])
        rotor3 = np.mat([self.identity[n] for n in self.rot3_perm])

        m = (plugbord *
             (row_perm_mat ** cnt1) * rotor1 * (col_perm_mat ** cnt1) *
             (row_perm_mat ** cnt2) * rotor2 * (col_perm_mat ** cnt2) *
             (row_perm_mat ** cnt3) * rotor3 * (col_perm_mat ** cnt3) *
             reflector *
             ((row_perm_mat ** cnt3) * rotor3 * (col_perm_mat ** cnt3)).I *
             ((row_perm_mat ** cnt2) * rotor2 * (col_perm_mat ** cnt2)).I *
             ((row_perm_mat ** cnt1) * rotor1 * (col_perm_mat ** cnt1)).I *
             plugbord)
        return m

    def get_cipher(self, plane):
        cipher = ''
        cnt = 0
        for char in plane:
            if char not in self.alphabet:
                cipher += char
                continue
            vec = [0] * self.size
            vec[self.char_dict[char]] = 1
            cnt2, cnt1 = divmod(cnt, self.size)
            cnt3, cnt2 = divmod(cnt2, self.size)
            cnt += 1
            m = self.get_matrix(cnt1, cnt2, cnt3 % self.size)
            vec = (vec * m).A[0]
            for n, x in enumerate(vec):
                if int(x) == 1:
                    cipher += self.alphabet[n]
                    break
        return cipher


if __name__ == "__main__":
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    plane = 'HELLO WORLD. MY NAME IS ALICE. NICE TO MEET YOU.'
    plug_perm = [2, 1, 4, 3, 5, 6, 7, 8, 9, 16, 11, 12, 20, 14,
                 15, 10, 17, 18, 19, 13, 21, 22, 23, 24, 25, 26]
    ref_perm = [26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15,
                14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    plug_perm = [x - 1 for x in plug_perm]
    ref_perm = [x - 1 for x in ref_perm]
    enigma = Enigma(plane, alphabet, plug_perm, ref_perm)
    cipher = enigma.get_cipher(plane)
    decrypt = enigma.get_cipher(cipher)
    print(cipher)
    print(decrypt)
