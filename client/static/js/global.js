// globals
let connection;
let audio;
// let map;
let path;
let run = true;
// let generateLocationButton = document.getElementById('generate-location')
// let useFakeLocation = false;

// user
let username;
let id = 'initial-id';
let latitude, longitude;
let jsonrpc_id = 0

const MY_COLOR = 'green';
const OTHER_COLOR = 'red';


// client methods
const INITIAL                 = 'initial'
const GET_ID                  = 'get_id'
const CREATE_GROUP            = 'create_group'
const SUBSCRIBE_TO_GROUP      = 'subscribe_to_group'
const START_METRONOME         = 'start_metronome'
const UPDATE_TEMP             = 'update_temp'
const STOP_METRONOME          = 'stop_metronome'
const DISCONNECT              = 'disconnect'
const PING                    = 'ping'

// server methods
const PLAY_SOUND              = 'play_sound';
const STOP_SOUND              = 'stop_sound';


