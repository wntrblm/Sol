// Timeout promise: https://italonascimento.github.io/applying-a-timeout-to-your-promises/
function asyncTimeout(ms, promise){
  // Create a promise that rejects in <ms> milliseconds
  const timeout = new Promise((resolve, reject) => {
    const id = setTimeout(() => {
      clearTimeout(id);
      reject(`asyncTimeout`);
    }, ms)
  });

  // Returns a race between our timeout and the passed in promise
  return Promise.race([
    promise,
    timeout
  ]);
}

// Javascript is silly and doesn't have a stream reader
// that reads line by line, so here we are... :/
class SerialLineTransformer extends TransformStream {
  constructor() {
    super({
      start() {}, 
      async transform(chunk, controller) {
        chunk = this.textDecoder.decode(await chunk);
        this.lineBuffer += chunk;
        let lines = this.lineBuffer.split('\r\n');
        this.lineBuffer = lines.pop();

        for (const line of lines) {
          controller.enqueue(line.trim());
        }
      },
      flush() {},
      textDecoder: new TextDecoder(),
      lineBuffer: '',
    });
  }
}

async function connectToSerial() {
  const requestOptions = {
    // Filter on devices with Sol's vendor and device ID,
    // though this doesn't actually do anything in chrome yet.
    filters: [{ vendorId: 0x239A, productId: 0x8062 }],
  };

  let port = await navigator.serial.requestPort(requestOptions);
  await port.open({ baudrate: 115200 });
  const decoder = new SerialLineTransformer();
  const reader = decoder.readable.getReader();
  port.readable.pipeThrough(decoder);
  const encoder = new TextEncoderStream();
  encoder.readable.pipeTo(port.writable);
  const writer = encoder.writable.getWriter();

  return {reader, writer};
}

async function callCircuitPythonFunction(reader, writer, expr) {
  await writer.write(`${expr}\r\n`);

  let output = '';

  while(true) {
    let {value, done} = (await reader.read());

    if(value === expr) {
      continue;
    }
    if(value === "done") {
      return output
    }
    output += value;

    if(done) return;
  }
}

async function callCircuitPythonFunctionWithTimeout(reader, writer, expr, timeout) {
  return await asyncTimeout(timeout, callCircuitPythonFunction(reader, writer, expr)); 
}

async function fetchCalibrationData(cpu_id)  {
  let response = await fetch(`https://files.winterbloom.com/sol/calibrations/${cpu_id}.py`);

  if(!response.ok) {
    throw `Could not find calibration data for CPU ID ${cpu_id}`;
  }
  
  let calibration_data = await response.text();

  // Remove comments and newlines so that this can be safely
  // transported over serial.
  calibration_data = calibration_data.replace(/^#.+$/gmi, '').replace(/\r?\n/gi, '');

  return calibration_data;
}

// Dom References
const connectButton = document.querySelector("#restore-connect-button");
const output = document.querySelector("#restore-output");


function clearStatus(){
  output.innerHTML = "";
}

function updateStatus(text) {
  let node = document.createElement("div");
  node.append(text);
  output.append(node);
}

async function connectAndStuff() {
  connectButton.disabled = true;

  const timeout = 5000; // 5 seconds.

  clearStatus();
  updateStatus(`Connecting...`);

  const {closePort, reader, writer} = (await connectToSerial());

  try {
    updateStatus(`Getting CPU ID...`);
    const cpu_id = await callCircuitPythonFunctionWithTimeout(
      reader, writer, "get_cpu_id()", timeout);

    updateStatus(`Getting Calibration data for CPU ID ${cpu_id}...`);
    const calibration_data = await fetchCalibrationData(cpu_id);

    updateStatus(`Writing calibration data...`);
    let result = await callCircuitPythonFunctionWithTimeout(
      reader, writer, `write_calibration_to_nvm("""${calibration_data}""")`, timeout);
    
      
    updateStatus(`Verifying calibration data...`);
    result = await callCircuitPythonFunctionWithTimeout(
      reader, writer, `read_calibration_from_nvm()`, timeout);

    updateStatus(`Restarting board...`);

    try {
      await callCircuitPythonFunction(reader, writer, `microcontroller.reset()`);
    }
    catch (err) {
      // It's okay if this fails, it's fine.
    }

    updateStatus(`Done!`);
  }
  catch (err) {
    switch(err) {
      case "asyncTimeout":
        updateStatus(`Timed out while talking to the device. Please refresh, reset it and try again.`);
        break;
      default:
        console.log(err);
        updateStatus(`Unknown error occurred. Please refresh, reset the device and try again.`);
        break;
    }
  }
  finally {
  }
}

connectButton.addEventListener("click", connectAndStuff, false);