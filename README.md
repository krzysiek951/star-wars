# Star Wars Explorer

Sample project to collect, transform and browse the data fetched from Star Wars API (SWAPI).

## Requirements

* Python 3.9+
* Docker

Visit official [Docker website](https://www.docker.com/) to download and install Docker on your operating system.

## Usage

### Installation

Clone the repository:

```shell
git clone https://github.com/krzysiek951/star-wars.git && cd star-wars
```

Copy `.env.example` file as `.env` and adapt settings inside

Build docker container:

```shell
docker-compose build
```

Run server inside docker container:

```shell
make start
```

### Basic commands

#### Run the server

```shell
make start
```

#### Stop the server

```shell
make stop
```

### Maintenance commands

#### Reset database

```shell
make reset-db
```

## Improvement suggestions

Time to complete this project was limited, so there are a lot of things that could be improved. You can consider the
following suggestions:

1. The application sends many requests to the API, so it would be reasonable to implement asynchronous requests.
2. With more data transformations, it would be worth making a separate class for them. I would consider using
   e.g. [builder design pattern](https://refactoring.guru/design-patterns/builder)  to make further transformations
   quite easy to implement and detach. 
3. Catching more exceptions to provide better feedback for the user. 
4. With catching more exceptions, it would be reasonable to make logging more comprehensive. 
5. Writing more tests to ensure everything works as supposed.