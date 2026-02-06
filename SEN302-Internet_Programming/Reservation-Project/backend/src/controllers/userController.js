import { createUser, getAllUsers, getUserById, updateUser, deleteUser } from '../models/userModel.js';


const handleResponse = (res, status, message, data) => {
    res.status(status).json({
        status,
        message,
        data
    });
}

export const createuser = async (req, res, next) => {
    const { username, email } = req.body;
    try {
        const newuser = await createUser(username, email);
        handleResponse(res, 201, 'User created successfully', newuser);
    } catch (err) {
        next(err);
    }
}

export const getallUsers = async (req, res, next) => {
    try {
        const users = await getAllUsers();
        handleResponse(res, 200, 'Users retrieved successfully', users);
    } catch (err) {
        next(err);
    }
}

export const getuserById = async (req, res, next) => {
    const { id } = req.params;
    try {
        const user = await getUserById(id);
        user
            ? handleResponse(res, 200, 'User retrieved successfully', user)
            : handleResponse(res, 404, 'User not found', null);
    } catch (err) {
        next(err);
    }
}

export const updateuser = async (req, res, next) => {
    const { id } = req.params;
    const { username, email } = req.body;
    try {
        const updateduser = await updateUser(id, username, email);
        updateduser
            ? handleResponse(res, 200, 'User updated successfully', updateduser)
            : handleResponse(res, 404, 'User not found', null);
    } catch (err) {
        next(err);
    }
}

export const deleteuser = async (req, res, next) => {
    const { id } = req.params;
    try {
        const result = await deleteUser(id);
        handleResponse(res, 200, result.message, null);
    } catch (err) {
        next(err);
    }
}

