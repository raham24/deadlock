const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const projectPath = args[0] ? path.resolve(args[0]) : process.cwd();
const pkgPath = path.join(projectPath, "package.json");

if (!fs.existsSync(pkgPath)) {
  console.error("❌ package.json not found in:", projectPath);
  process.exit(1);
}

const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));

// Determine if it's React or Node
const isReact = pkg.dependencies?.react || pkg.devDependencies?.react;
const port = isReact ? 3000 : 3000;
const startCommand = pkg.scripts && pkg.scripts.start ? ["npm", "start"] : ["node", pkg.main || "index.js"];

const dockerfile = isReact
  ? `
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE ${port}
RUN npm run build
CMD ["npx", "serve", "build"]
  `.trim()
  : `
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE ${port}
CMD ${JSON.stringify(startCommand)}
  `.trim();

fs.writeFileSync(path.join(projectPath, "Dockerfile"), dockerfile);

console.log("✅ Dockerfile generated at", path.join(projectPath, "Dockerfile"));
