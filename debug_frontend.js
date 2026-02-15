// Simple script to check what the frontend is actually using
const fs = require('fs');
const path = require('path');

// Read the .env file
const envPath = path.join(__dirname, 'frontend', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
console.log('Frontend .env content:');
console.log(envContent);

// Check if there are any hardcoded URLs in the API service
const apiPath = path.join(__dirname, 'frontend', 'src', 'services', 'api.js');
const apiContent = fs.readFileSync(apiPath, 'utf8');
console.log('\nAPI service content:');
console.log(apiContent);

// Check for any other config files
const configFiles = [
  'frontend/src/config.js',
  'frontend/src/constants.js',
  'frontend/public/env.js'
];

configFiles.forEach(file => {
  const fullPath = path.join(__dirname, file);
  if (fs.existsSync(fullPath)) {
    console.log(`\n${file} content:`);
    console.log(fs.readFileSync(fullPath, 'utf8'));
  }
});