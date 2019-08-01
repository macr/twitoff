
 function postJSON(url, data){
    return fetch(url,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
  
  }
export function hello(){

}
function appReducer (state, action){
  switch(action.type){
    case 'setUsers': return {
      ...state,
      users: action.payload
    }
    default:
      return state;
  }
}

export  {postJSON, appReducer}