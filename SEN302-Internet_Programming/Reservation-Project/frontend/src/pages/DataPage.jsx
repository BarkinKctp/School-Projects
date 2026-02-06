import { UserCard } from "../components/UserCard";
import { CreateUserForm } from "../components/CreateUserForm";
import { useState } from "react";
// import { useEffect } from "react"; uncomment when using useEffect
import '../css/DataPage.css';
import { fetchUsers } from "../services/userService";

function DataPage() {

    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [empty, setEmpty] = useState(false);

    /*
    // TODO: useEffect for auto-loading users on page mount
      useEffect(() => {
        async function autoloadUsers(){
            setError(null);
            setIsLoading(true);
            try {
                const data = await fetchUsers();
                setUsers(data);
                setEmpty(data.length === 0);
            } catch (error) {
                console.error('Error fetching users:', error);
                setError(error);
            } finally {
                setIsLoading(false);
            }
        }
        autoloadUsers();
     }, []);

    // upon use, remove e parameter from loadUsers function
    */

    async function loadUsers(e) {
        e.preventDefault();
        setError(null);
        try {
            setIsLoading(true);
            const data = await fetchUsers();
            setUsers(data);
            setEmpty(data.length === 0);
        } catch (error) {
            console.error('Error fetching users:', error);
            setError(error);
        }
        finally {
            setIsLoading(false);
        }
    }

    function onUserEdited (userId, updatedData) {
        setUsers((prevUsers) =>
            prevUsers.map((user) =>
                user.id === userId ? { ...user, ...updatedData } : user
            )
        );
    }
    
    function onUserDeleted(userId) {
        setUsers((prevUsers) => 
            prevUsers.filter((user) => 
                user.id !== userId)
    );
    }

    return (
        <div className="data-page">
            <h2>User Data</h2>

                {/* Remove while using load effect */}
                <button className="get-user-list" onClick={loadUsers} disabled={isLoading}>
                    {isLoading ? 'Loading...' : 'Get User List'}
                </button>

                <CreateUserForm 
                onUserCreated={(newUser) => 
                setUsers((prevUsers) => 
                [...prevUsers, newUser])} />

            {error && <p className="error-message">Error: {error.message}</p>}
            {empty && <p className="empty-message">No users to display.</p>}

            <div className="user-cards-container">
                {users.map((user) => (
                    <UserCard 
                        key={user.id}
                        user={user}
                        onUserEdited={onUserEdited}
                        onUserDeleted={onUserDeleted}
                    />
                ))}
            </div>
        </div>
    );

}
    


export default DataPage;
