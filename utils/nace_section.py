class Nace:
    @staticmethod
    def get_nace_section(nace_code):
        code_str = str(nace_code).zfill(2)
        code = int(code_str[:2])
        if 1 <= code <= 3:
            return 'A'
        elif 5 <= code <= 9:
            return 'B'
        elif 10 <= code <= 33:
            return 'C'
        elif 35 <= code <= 35:
            return 'D'
        elif 36 <= code <= 39:
            return 'E'
        elif 41 <= code <= 43:
            return 'F'
        elif 45 <= code <= 47:
            return 'G'
        elif 49 <= code <= 53:
            return 'H'
        elif 55 <= code <= 56:
            return 'I'
        elif 58 <= code <= 63:
            return 'J'
        elif 64 <= code <= 66:
            return 'K'
        elif 68 <= code <= 68:
            return 'L'
        elif 69 <= code <= 75:
            return 'M'
        elif 77 <= code <= 82:
            return 'N'
        elif 84 <= code <= 84:
            return 'O'
        elif 85 <= code <= 85:
            return 'P'
        elif 86 <= code <= 88:
            return 'Q'
        elif 90 <= code <= 93:
            return 'R'
        elif 94 <= code <= 96:
            return 'S'
        elif 97 <= code <= 98:
            return 'T'
        elif code == 99:
            return 'U'
        else:
            return 'Unknown'
