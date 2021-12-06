# Hitory
Hitory sat solver

# Get started
```bash
  git clone git@github.com:quatpv/Hitori.git
  cd Hitori  
```

# Install and run server
```bash
  sudo apt install minisat
  pip install fastapi
  pip install "uvicorn[standard]"
  # and install other lib for python if needed

  # start server
  uvicorn main:app --reload
```

# Install and run client
```bash
  cd client/
  npm install # or yarn 
  npm run dev
```
Go to http://localhost:3000 and enjoy it!
