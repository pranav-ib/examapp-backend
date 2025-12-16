from fastapi import APIRouter
from pydantic import BaseModel
from supabase_client import supabase
import hashlib
import uuid

router = APIRouter()

class RecruiterRegister(BaseModel):
    name : str
    email : str
    password : str

class RecruiterLogin(BaseModel):
    email : str
    password : str

def hash_password(password : str):
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/recruiter/register")
def recruiter_register(data: RecruiterRegister):

    # Check duplicate email
    existing = (
        supabase.table("recruiters")
        .select("*")
        .eq("email", data.email)
        .execute()
    )

    if existing.data:
        return {"error": "Email already registered"}

    # Hash password
    hashed = hash_password(data.password)

    # Insert recruiter into Supabase
    result = (
        supabase.table("recruiters")
        .insert({
            "name": data.name,
            "email": data.email,
            "password_hash": hashed
        })
        .execute()
    )

    recruiter_id = result.data[0]["id"]

    return {
        "status": "OK",
        "message": "Recruiter registered successfully",
        "recruiter_id": recruiter_id
    }



@router.post("/recruiter/login")
def recruiter_login(data : RecruiterLogin):

    hashed = hash_password(data.password)
    try:
        res = (
            supabase.table("recruiters")
            .select("*")
            .eq("email", data.email)
            .eq("password_hash", hashed)
            .single().execute()
        )

        result = res.data

        if result is None:
            return {"error" : "Invalid credentials"}
        
        return {"status": "OK", 
                "recruiter_id": result["id"],
                "name": result["name"],
                "email": result["email"]
        }
    except Exception as e:
        return {"error" : "Invalid credentials"}
