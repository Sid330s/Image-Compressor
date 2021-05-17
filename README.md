# Image-Compression-Huffman
Converts images to text, then compresses the text file using Huffman compression

A web app built on Flask that lets users upload images, and download the compressed text file. Users can upload the compressed
file back again and get the decompressed image back. Uses **Huffman Compression** technique to compress the bits of each pixel
generated, using Heaps in C. Works only for grayscale images.

```sh
# Windows users can follow this: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
$ set FLASK_APP=node_server.py
$ flask run --port 8000
```

### Technology Stack
* Python (*Flask*, *PIL*)
* C
* HTML
* CSS
* Javascript (*AJAX*, *JSON*)
