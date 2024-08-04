# Game of Life

[**Conway's Game of Life**](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) written in **Python**, using [Taichi lang](https://www.taichi-lang.org).

![Conway's Game of Life](screenshot.png)

## Features

### Capabilities

-   Standard [rules](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules)
-   [Finite field as todorial array](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Algorithms:~:text=In%20principle%2C%20the,M%C3%B6bius%20strip.)
-   Randomize, clear field
-   Pause simulation
-   Draw cells

### Settings

-   Field size
-   Cells color
-   Start condition
-   Backend computing
-   Profiling
-   Field generation

## Installation

### Prerequisites

As the project is written in **Python**, you must have [Python interpreter](https://www.python.org/downloads/) installed on machine to run code.<br>

> [!IMPORTANT]  
> Not all Python versions work with Taichi. Which specific do are listed on [official website](https://docs.taichi-lang.org/docs/hello_world#prerequisites). To avoid further conflicts [release 3.10.11](https://www.python.org/downloads/release/python-31011/) is recommended.

### Repository

To get a local copy of repository open terminal and execute `git clone` command:

```
git clone https://github.com/wivest/Game-of-Life.git
```

### Packages

Some external Python packages are required, including **Taichi**. To install them open cloned directory in terminal:

```
cd Game-of-Life
```

> [!TIP]  
> _Optional step. Recommended to avoid package versions conflicts._<br>
> To manage Python packages **virtual environment** can be created. More information can be found [here](https://docs.python.org/3/library/venv.html).

To collect missing packages execute `pip install` command:

```
pip install -r requirements.txt
```

## Run the project

Open project folder in terminal and launch `main.py` file by executing `python` command:

```
python main.py
```

### Actions in-game

-   Randomize by pressing `R` key.
-   Clear by pressing `C` key.
-   Pause by pressing `Spacebar` key.
-   Draw by pressing and dragging left mouse button.
-   Erase by pressing and dragging right mouse button.

## Configuration

By editing parameters in [`parameters.json`](parameters.json) you can customize behaviour of application. Here available ones for user are listed:

| Name         | Type     | Description                                                                                     |
| ------------ | -------- | ----------------------------------------------------------------------------------------------- |
| `columns`    | `int`    | Number of field columns.<br>_Default: `1024`_                                                   |
| `rows`       | `int`    | Number of field rows.<br>_Default: `512`_                                                       |
| `arch`       | `string` | Backend architecture used by Taichi.<br>_Suggested: `"gpu"` and `"cpu"`._<br>_Default: `"gpu"`_ |
| `profiling`  | `bool`   | Enable profiling of Taichi kernel in form of terminal output.<br>_Default: `false`_             |
| `alive`      | `Array`  | Alive cell color in RGB format.<br>_Default: `[255, 255, 255]`_                                 |
| `dead`       | `Array`  | Dead cell color in RGB format.<br>_Default: `[0, 0, 0]`_                                        |
| `percentage` | `float`  | Percentage of alive cells when randomizing field.<br>_Default: `0.1`_                           |
