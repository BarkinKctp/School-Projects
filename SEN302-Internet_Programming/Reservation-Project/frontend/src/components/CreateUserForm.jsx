import { useState } from 'react';
import '../css/CreateUserForm.css';
import { createUser } from '../services/userService';

function CreateUserForm({ onUserCreated }) {

    const [isCreating, setIsCreating] = useState(false);
    const [validationError, setValidationError] = useState(null);
    const [formEditData, setFormEditData] = useState({
        username: '',
        email: ''
    });

    // TODO: DUPLICATE - will move to utils/validation.js
    function validateForm(data) {
        if (!data.username.trim() || !data.email.trim()) {
            setValidationError('Both fields are required.');
            console.error(validationError);
            return false;
        }
        if (!data.username || data.username.length < 3) {
            setValidationError('Username must be at least 3 characters long.');
            console.error(validationError);
            return false;
        }
        if(!data.email || !/\S+@\S+\.\S+/.test(data.email)) {
            setValidationError('Please enter a valid email address.');
            console.error(validationError);
            return false;
        }
        setValidationError(null);
        return true;
    }

    // TODO: DUPLICATE - will move to utils/formHelpers.js
    function handleChange(e){
        setFormEditData({
            ...formEditData,
            [e.target.name]: e.target.value
        });  
    }

    async function createNewUser(e) {
        e.preventDefault();
        if (!validateForm(formEditData)) {
            return;
        }
        setIsCreating(true);
        try {
            const newUser = await createUser(formEditData);
            onUserCreated(newUser);
            setFormEditData({ username: '', email: '' });
        } catch (error) {
            setValidationError(error.message || "Failed to create user");
        } finally {
            setIsCreating(false);
        }
    }

    return (
        <form className="create-user-form" onSubmit={createNewUser}>
            {validationError && <p className="validation-error">{validationError}</p>}
            <input 
                type="text" 
                name="username" 
                value={formEditData.username} 
                onChange={handleChange} 
                placeholder="Name" required />
            <input 
                type="email" 
                name="email" 
                value={formEditData.email} 
                onChange={handleChange} 
                placeholder="Email" required />
            <button type="submit" disabled={isCreating}>Create User</button>
            <button type="button" onClick={() => {
                        setIsCreating(false);
                        setFormEditData({ username: '', email: '' });
                        setValidationError(null);
                    }} disabled={isCreating}>Cancel</button>
        </form>

    );
}

export { CreateUserForm };
