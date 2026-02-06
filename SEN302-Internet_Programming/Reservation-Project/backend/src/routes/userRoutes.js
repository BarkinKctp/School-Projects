import express, { Router } from 'express';
import { getallUsers, createuser, getuserById, updateuser, deleteuser } from '../controllers/userController.js';
import validateUser from '../middlewares/inputValidator.js';

const router = express.Router();

// Sample user route

router.get("/user", getallUsers);
router.post("/user", validateUser, createuser);
router.get("/user/:id", getuserById);
router.put("/user/:id", validateUser, updateuser);
router.delete("/user/:id", deleteuser);

export default router;
