# Library System API

Library Website API built using Django, Django Rest Framework, Rest Knox Authentication and Django Filters.

The API methods can be used by frontend code to allow users and librarians to access the books available in the library.

Librarians have access for adding new books, authors, categories, publications and book copies. While normal users can access the available books in the library, search and filter through them and borrow copies of books.

## Installing Using Docker

1. Run `git clone https://github.com/EliasObeid9-02/library_system.git` to clone the repository.
2. Run `cd library_system` to change into the code directory.
3. Copy the `.env.example` file into `.env` and edit the variables to fit your needs, the mail variables are required for the password reset methods.
4. Run `docker compose build` to build the images.
5. Run `docker compose up` to launch the containers.

To stop the containers press `Ctrl+C` and run `docker compose stop`, optionally run `docker compose down` to remove the containers.

To the run the application again run `docker compose up`.

To access the website use the URL `http://127.0.0.1:8000/`
