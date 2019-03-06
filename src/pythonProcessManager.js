const path = require('path')
const fs = require('fs')
const child_process = require('child_process')

/*****

Section 1: Class Definition

PythonProcessManager: Class for managing the creation 
and destruction of Python processes

*****/

class PythonProcessManager {

  constructor () {
    this.pythonProcess = null
    this.pythonServerPort = 4242
  }

  startPythonProcess (filename) {
    let pythonPath = getPythonPath(filename)
    console.log(pythonPath)
    if (isPackaged()) {
      // If Python is packaged, just run the executable
      this.pythonProcess = child_process.execFile(pythonPath) // had path
    } else {
      // Otherwise run the terminal command 'python' with the script's path
      this.pythonProcess = child_process.spawn('python', [pythonPath])
    }

    // Output to console on success/failure of Python process spawn
    if (this.pythonProcess != null) {
      console.log('Python process started on port ' + this.pythonServerPort)
    } else {
      console.log('Error! Python process failed to start :(')
    }

    

  }

  stopPythonProcess () {
    if (this.pythonProcess != null) {
      this.pythonProcess.kill()
      this.pythonProcess = null
      console.log('Python process terminated')
    }
  }

}

/*****

Section 2:

Helper functions used by the PythonProcessManager Class
but are not needed in external modules

*****/

/** Hard-coded constants that should probably be 
made into environment variables as they are subject to change **/

const PYTHON_DIST_FOLDER = 'pydist'
const PYTHON_FOLDER = 'py'
const PYTHON_MODULE = 'server' // without .py suffix

/** Function that checks if the Python code has been packaged by 
 looking for a dist folder **/
const isPackaged = () => {
  return fs.existsSync(path.join(__dirname, PYTHON_DIST_FOLDER))
}

/** Function that returns the full path of the 
Python script/.exe/module to be executed **/
const getPythonPath = (filename) => {
  let pythonPath = null
  if (!isPackaged()) {
    // Not packaged - return the main .py file
    pythonPath = path.join(__dirname, '../src/', PYTHON_FOLDER, filename + '.py')
  } else if (process.platform === 'win32') {
    // Packaged and running Windows - return .exe
    pythonPath = path.join(__dirname, PYTHON_DIST_FOLDER, filename, filename + '.exe')
  } else {
    // Packaged and running anything else - return Python module
    pythonPath = path.join(__dirname, PYTHON_DIST_FOLDER, filename, filename)
  }
  return pythonPath
}

export default PythonProcessManager