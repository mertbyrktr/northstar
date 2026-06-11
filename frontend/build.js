const fs = require('fs');
const path = require('path');

const srcDir = __dirname;
const distDir = path.join(__dirname, 'dist');

function cleanDirectory(directory) {
  if (fs.existsSync(directory)) {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

function ensureDirectoryExistence(filePath) {
  const dirname = path.dirname(filePath);
  if (fs.existsSync(dirname)) {
    return true;
  }
  ensureDirectoryExistence(dirname);
  fs.mkdirSync(dirname);
}

function copyFile(src, dest) {
  ensureDirectoryExistence(dest);
  fs.copyFileSync(src, dest);
  console.log(`Copied: ${path.relative(srcDir, src)} -> ${path.relative(srcDir, dest)}`);
}

function copyDir(src, dest) {
  ensureDirectoryExistence(dest);
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFile(srcPath, destPath);
    }
  }
}

console.log('Cleaning existing dist directory...');
cleanDirectory(distDir);

console.log('Copying static assets...');
copyFile(path.join(srcDir, 'index.html'), path.join(distDir, 'index.html'));
copyFile(path.join(srcDir, 'style.css'), path.join(distDir, 'style.css'));

if (fs.existsSync(path.join(srcDir, 'js'))) {
  copyDir(path.join(srcDir, 'js'), path.join(distDir, 'js'));
}

console.log('Build completed successfully! Assets are ready in frontend/dist/');
