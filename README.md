# HIT137_Assignment3

A repository for our group assignment 3 for the HIT137 class.

## Deadline: 18/10/2024, 17:00

## Table of Contents

- [Setting Up the Environment](#setting-up-the-environment)
  - [Virtual Environment](#virtual-environment)
  - [Installing Requirements](#installing-requirements)
  - [Updating Requirements](#updating-requirements)
- [Task Briefing](#task-briefing)

## Setting up the environment

### Virtual Environment

1. Create a virtual environment

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment
    - On Windows:

      ```bash
      Set-ExecutionPolicy Unrestricted -Scope Process
      .\.venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source .venv/bin/activate
      ```

   *Note: If your IDE automatically uses the virtual environment, you may not need to activate it manually. However, if you are using a terminal outside of your IDE, you will need to activate the virtual environment each time you open a new terminal session.*

### Installing Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Updating Requirements

If new pip packages are required for the assignment, please install the package and update the `requirements.txt` file using the following command:

```bash
pip freeze > requirements.txt
```

## Task Briefing

### Task 1

Create a tkinter application using Object Oriented Programming Concepts.

### Task 2

Create a side scrolling 2D game using Pygame.
