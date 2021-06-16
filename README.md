# pynCoder

## Contribution

Contributions are welcome, just send me an email and we will work something out together!

## Description

`pynCoder` is a CLI tool that allows you to encode/decode strings or files through the command line. <br>
I made this tool in order to simplify the process of decoding various messages or flags that can be found in some CTF challenges.<br><br>
We all know that CTF creators tends to be evil sometimes by encoding messages with multiple algorithm on top of each other,<br>
Making the process a bit tedious in the long run. <br>

---

## Usage

- Get Help: <br>
  &emsp;`./pynCoder.py -h`<br><br>
- Encode a String in Base64 : <br>
  &emsp;`./pynCoder.py -e "Hello World!" -b64`<br><br>
- Decode a String from Base64 : <br>
  &emsp;`./pynCoder.py -d "SGVsbG8gV29ybGQh" -b64`<br><br>
- Encode a String in Base64 4 times : <br>
  &emsp;`./pynCoder.py -e4 "Hello World!" -b64`<br><br>
- Decode a String from Base64 4 times : <br>
  &emsp;`./pynCoder.py -d4 "VlRCa1YyTXlTa2hQUjJSWFRXcHNOVmxyWkZKaFFUMDk=" -b64`<br><br>
- Decode a String by Auto-Detection : <br>
  &emsp;`./pynCoder.py -d 'u*)rc{#pu*"rc{y~u*"rc{y~u*"ra{y}tp)$p{#}u&"ra{y}tp)ra{#pu*($c{#pu&)rcxq}u*($c{y}' -a`<br><br>
- Encode a File in Rot-47 : <br>
  &emsp;`./pynCoder.py -E README.md -r47`<br><br>
- Decode a File from Rot-47 : <br>
  &emsp;`./pynCoder.py -D README.md -r47`<br><br>

---

## Functionalities

There's an 'Auto-Detect' feature implemented (which is still experimental, so it might still be prone to errors), that allows to decode a strings in cycles.<br>
The Auto-Detect feature is only working in `String Decoding mode` for now and will be implemented in `File Decoding mode` eventually<br><br>
Example :<br> If we supply a Base64 string which was encoded 5 times in a row, then the Auto-Detect feature <br>
will keep decoding the string until it reaches the string's original form (considering that the original string was written in normal plain text)<br><br>
It can also detect some chained encoding like : Plain Text -> Hex -> Morse -> Base64 -> Base64 -> Base64<br>

---

## Supported Encodings

`pynCoder` supports the following encodings as for now :

- Morse
- Hex (Base16)
- Base32
- Base64
- Rot13
- Rot18
- Rot47

### Note: pynCoder cannot Auto-Detect any of the Rotary algorithm (Rot13, Rot18, Rot47) for the moment.

---

## Examples

### Get Help

![Example 1](img/pynCoder-help.png) <br><br>

### Auto-Detect feature applied in String Decoding mode

![Example 2](img/pynCoder-Auto.png) <br><br>

### Hex encoding over 3 iterations

![Example 3](img/pynCoder-hex-3.png) <br>

### Hex decoding over 3 iterations

![Example 4](img/pynCoder-hex-d3.png) <br>
