import sys
import re

class CreeportInterpreter:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.vars = {}
        self.labels = {}
        self.current = 0

    def load(self):
        with open(self.filename, 'r') as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if line:
                    self.lines.append(line)
                    if re.match(r'^[A-Za-z_][A-Za-z0-9_]*:$', line):
                        label = line[:-1]
                        self.labels[label] = len(self.lines) - 1

    def run(self):
        while self.current < len(self.lines):
            line = self.lines[self.current]
            if line.endswith(":"):  # label, já processado
                self.current += 1
                continue
            if line.startswith("PRINT "):
                expr = line[6:].strip()
                print(self.eval_expr(expr))
            elif line.startswith("LET "):
                parts = line[4:].split("=", 1)
                if len(parts) != 2:
                    raise SyntaxError(f"Invalid LET statement: {line}")
                var, expr = parts
                var = var.strip()
                self.vars[var] = self.eval_expr(expr.strip())
            elif line.startswith("IF "):
                m = re.match(r'IF (.+) THEN (\w+)', line)
                if not m:
                    raise SyntaxError(f"Invalid IF statement: {line}")
                condition, label = m.groups()
                if self.eval_expr(condition):
                    if label not in self.labels:
                        raise ValueError(f"Label not found: {label}")
                    self.current = self.labels[label]
                    continue
            elif line.startswith("GOTO "):
                label = line[5:].strip()
                if label not in self.labels:
                    raise ValueError(f"Label not found: {label}")
                self.current = self.labels[label]
                continue
            elif line == "END":
                break
            else:
                raise SyntaxError(f"Unknown command: {line}")
            self.current += 1

    def eval_expr(self, expr):
        try:
            return eval(expr, {}, self.vars)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expr}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python creeport.py <file.cree>")
        sys.exit(1)
    interpreter = CreeportInterpreter(sys.argv[1])
    interpreter.load()
    interpreter.run()
