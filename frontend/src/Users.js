
import React, {useContext, useState} from 'react'
import {Link} from 'react-router-dom'
import Context from './Context'
import {postJSON} from './helpers'
function Users({users}){
    const dispatch = useContext(Context)
    const [user, setUser] = useState('');
    const [loading, setLoading] = useState(false);
    async function addUser(user){
      setLoading(true)
      const r = await postJSON('/api/users', user);
      const data = await r.json();
      const users = data.map(user=> ({...user, loading:false}))
      dispatch({type: 'setUsers', payload: users});
      setLoading(false)
    }
      return(
      <div className='twitter-users'>
          <h3>Tweeter Users</h3>
        <div>
          {users.map((user)=>(
            <Link  key={user.id} to={`/user/${user.id}`}>
                <li>{user.username}</li>
            </Link>
          ))}
        </div>
      <div>
        <h3>Add/Update User</h3>
        User: <input type='text' value={user} onChange={(e)=>setUser(e.target.value)}/>
        <button disabled={loading} onClick={()=>addUser(user)} >{loading ? 'Loading...': 'Add/Update'}</button>
      </div>
      </div>
      
    )
  }
  export default Users