# frontend
This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).


## Requirements

1. [Node v14.16.1 LTS](https://nodejs.org/en/)
2. [Yarn v1](https://classic.yarnpkg.com/en/)

## Installation

Run `yarn` to install all dependencies

## Development Build

To run the development server, simply run:

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Production Build

We are using Docker container for production build.

1. Get [Docker](https://docs.docker.com/get-docker/)
2. Build the Docker image by running: `docker build . -t comp90024-frontend`
3. Run a Docker instance by running: `docker run -p 3000:3000 comp90024-frontend`
