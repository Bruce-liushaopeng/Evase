# Use an official Node.js runtime as a parent image
FROM node:16.13.2-alpine

ENV REACT_APP_TEST=env_set_success

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the application
RUN npm run build

# Expose the port on which the application will run
EXPOSE 3000

# Define the command to start the application
CMD ["npm", "start"]