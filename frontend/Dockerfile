# Stage 1: Build the React application
FROM node:16 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend directory contents into the container
COPY . .

# Build the project
RUN npm run build

# Stage 2: Serve the application using a Node.js server
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Install the serve package globally
RUN npm install -g serve

# Copy the build output from the previous stage
COPY --from=build /app/build /app/build

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the app
CMD ["serve", "-s", "build", "-l", "tcp://0.0.0.0:3000"]
