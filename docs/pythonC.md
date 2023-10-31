# Metodologia di scrittura .C per Python/C API (CPython)

---
## parametri input 
### Validazione e definizione

La funzione PyArg_ParseTuple() usa una stringa di formato per interpretare i valori in una tupla di argomenti. Questa stringa di formato può contenere diversi caratteri (o combinazioni di caratteri) che rappresentano vari tipi di dati. Ecco alcuni dei formati comuni utilizzati con PyArg_ParseTuple():

#### Integers:
"b": char  
"h": short int  
"i": int  
"l": long int  
"B": unsigned char  
"H": unsigned short int  
"I": unsigned int  
"k": unsigned long  
"L": long long  
"K": unsigned long long    

#### Floating point:
"f": float (ma in realtà viene estratto come un double)  
"d": double    

#### Strings:
"s": string (char*); non contiene byte zero  
"z": string (char*) o None (convertito in NULL)  
"s#" e "z#": come "s" e "z", ma ritorna anche la lunghezza    

#### Python objects:
"O": oggetto (ritorna un PyObject*)  
"O!": oggetto di un tipo specificato, es: "O!" &PyList_Type per verificare che sia una lista   

#### Buffers:
"y": bytes  
"y*": qualunque oggetto buffer-contiguamente-orientato  
"y#": bytes e la sua lunghezza    

#### Altri:
"c": char (un singolo carattere)  
"p": int (come un booleano, per "predicate")  
"C": int (come un char non segnato)  
"n": Py_ssize_t (utile per lunghezze e indici)  