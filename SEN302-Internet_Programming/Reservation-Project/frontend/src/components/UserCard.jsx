import { useState } from 'react';
import '../css/UserCard.css';
import { editUser, deleteUser} from '../services/userService';

function UserCard({ user, onUserDeleted, onUserEdited }) {

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [validationError, setValidationError] = useState(null);
    const [formEditData, setFormEditData] = useState({
        username: user.username,
        email: user.email
    });

    
    function openEditForm() {
        setIsEditing(true);
    }

    function openDeleteConf() {
        setIsDeleting(true);
    }

    // TODO: DUPLICATE - will move to utils/formHelpers.js
    function handleChange(e){
        setFormEditData({
            ...formEditData,
            [e.target.name]: e.target.value
        });  
    }

    // TODO: DUPLICATE - will move to utils/validation.js
    function validateForm() {
        if (!formEditData.username.trim() || !formEditData.email.trim()) {
            setValidationError('Both fields are required.');
            return false;
        }
        if (!formEditData.username || formEditData.username.length < 3) {
            setValidationError('Username must be at least 3 characters long.');
            return false;
        }
        if(!formEditData.email || !/\S+@\S+\.\S+/.test(formEditData.email)) {
            setValidationError('Please enter a valid email address.');
            return false;
        }
        if(formEditData.username === user.username && formEditData.email === user.email) {
            setValidationError('No changes detected.');
            return false;
        }
        setValidationError(null);
        return true;
    }

    async function submitEditForm(e) {
        e.preventDefault();
        if (!validateForm()) {
            return;
        }
        setIsSubmitting(true);  // disable button
        try {
            await editUser(user.id, formEditData);
            onUserEdited(user.id, formEditData);
            setIsEditing(false);
        } catch (error) {
            setValidationError(error.message || "Failed to edit user");
        } finally { setIsSubmitting(false); }  // re-enable
    }
    
    async function submitDeleteForm(e) {
        e.preventDefault();
        try {
            setIsSubmitting(true);  // disable button
            await deleteUser(user.id);
            onUserDeleted(user.id);  
            setIsDeleting(false);
        } catch (error) {
            console.error('Error deleting user:', error);
        } finally { setIsSubmitting(false); }  // re-enable
    }

    return (
        <div className="user-card">
            <h3>{user.username}</h3>
            <p>Email: {user.email}</p>
            <button className="edit-button" onClick={openEditForm}>Edit</button>
            <button className="delete-button" onClick={openDeleteConf}>Delete</button>
            {isEditing && (
                <form className="edit-form" onSubmit={submitEditForm}>
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
                    <button type="submit" disabled={isSubmitting}>Submit</button>
                    <button type="button" onClick={() => {
                        setIsEditing(false);
                        setFormEditData({ username: user.username, email: user.email });
                        setValidationError(null);
                    }} disabled={isSubmitting}>Cancel</button>
                </form>
            )}
            {isDeleting && (
                <form className="delete-confirmation" onSubmit={submitDeleteForm}>
                    <input type="hidden" name="User id:" value={user.id} />
                    <p>Are you sure you want to delete this user?</p>
                    <button type="submit" disabled={isSubmitting}>Yes</button>
                    <button type="button" onClick={() => setIsDeleting(false)} disabled={isSubmitting}>Cancel</button>
                </form>
            )}
            {validationError && <p className="validation-error">{validationError}</p>}
        </div>
    );
}

export { UserCard };