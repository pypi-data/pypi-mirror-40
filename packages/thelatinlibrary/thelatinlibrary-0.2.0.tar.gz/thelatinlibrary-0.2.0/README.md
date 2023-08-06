# thelatinlibrary <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/264498ee-73ce-49d8-8ebc-f1f845fff514/d9clbzg-a94e9f45-a32c-4fef-a56d-64e8040539c9.png" width=40 height=40/>

[![License: GNU General Public License v3 (GPLv3)](https://img.shields.io/badge/License-GNU%20General%20Public%20License%20v3%20(GPLv3)-blue.svg)](./LICENSE) [![Developer: Hearot](https://img.shields.io/badge/Developer-%20Hearot-red.svg)](https://hearot.it)

Use [thelatinlibrary](http://www.thelatinlibrary.com) to search all you want. The best database of latin texts has landed on [Python](https://python.org).

## Install

### Via GitHub

Use this piece of code:

```
pip install git+https://github.com/hearot/thelatinlibrary.git
```

### Downloading files

*In primis* (from Latin, “firstable”), **clone** the repository:

```
git clone https://github.com/hearot/thelatinlibrary.git
```

Then, change directory:

```
cd thelatinlibrary
```

And finally, install the **package**:

```
sudo python3 setup.py install
```

## Example

```python
import thelatinlibrary

authors = thelatinlibrary.get_authors()

for author in authors:
    print(author, author.works)
    
caesar = thelatinlibrary.get_author_by_name("caesar")
print(caesar.works)
```

## License

This library is licensed by the [GNU General Public License v3 (GPLv3)](LICENSE). [The Latin Library](http://www.thelatinlibrary.com) is not affiliated with this project. The [logo](https://www.deviantart.com/undevicesimus/art/Polandball-Icon-Romeball-565346284) used in the title has been created by [undevicesimus](https://www.deviantart.com/undevicesimus).
