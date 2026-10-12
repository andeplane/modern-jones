# Primer: reading these SCI disassemblies (Jones in the Fast Lane, Sierra SCI 1.000.060)

Files: scriptNNN.asm (disassembled bytecode, one per script), ALL_TEXT.txt (text resources: `=== text.N` then `index string`).
Each .asm has: exports, LOCALS (script-local variable initial values; script000's locals ARE the game GLOBALS, so `lag 520` = global[520]),
OBJECT/CLASS entries with resolved properties, then code. `;;; method obj::sel` marks method starts, `;;; export #n` exported procs.

VM basics (stack machine, accumulator "acc"):
- push / pushi N / push0/1/2 / pushSelf push values; `push` pushes acc. ldi N loads acc.
- Var ops: [l|s|+|-][a|s][g|l|t|p][i]  e.g. lag 5 = load global5 into acc; lsl 3 = push local3; sat 1 = store acc to temp1;
  lap 1 = param 1 (lap 0 = argc); +ag = increment global then load; 'i' suffix = indexed by acc (array: var[base+acc]).
- Binary ops (add, sub, mul, div, mod, lt?, gt?, eq? ...) pop one value from stack as LEFT operand, acc as RIGHT; result in acc.
  e.g. `lsg 10; ldi 5; mul` -> acc = g10*5.  `push; ldi 3; lt?` -> acc = (prev acc < 3).
- bt/bnt = branch if acc true/false. call Lxxxx, n = local procedure call with n bytes of args (n/2 args) already pushed.
- callk K, n = kernel call (name annotated). Random(lo,hi) is kernel "Random". Format/Print/Display handle text.
  Text refs are often (textResourceNumber, index) pairs pushed before Format/Print: look the pair up in ALL_TEXT.txt.
- send n: message send to the object in acc. Arguments pushed before it are groups of (selector, argc, args...).
  `pushi 43 ; sel:number / push1 / pushi 100 / lofsa obj / send 6` = obj.number(100).
  `self n` sends to self, `super C, n` to superclass. `class N` loads class N into acc.
- pToa/aTop etc = read/write property of self (annotated prop:name). lofsa = address of object or string in this script (annotated).
- calle S, E, n = call export E of script S. callb E, n = call export E of script 0.
- Annotations `; sel:xxx` after pushi are only guesses when the number is a selector; ignore them for plain numeric constants.
Objects with price=, basePrice=, wage etc. carry data directly in props.
- Note: byte-form ldi/pushi operands are printed unsigned; a byte ldi of 255 may really mean -1.
