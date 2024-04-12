import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";

function Register() {
    const navigate = useNavigate();
    // Add your form submit handler here
    const handleSubmit = (event) => {
        event.preventDefault();
        // Collect data from the form and send it to your backend here
        // Make sure to add the role as 'customer'
    };

    return (
        <div className='h-screen flex justify-center items-center'>
            <Card className='w-[460px]'>
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl">Create an account</CardTitle>
                    <CardDescription>
                        Enter your detials below to create your account
                    </CardDescription>
                </CardHeader>

                <CardContent as="form" onSubmit={handleSubmit} className="grid gap-4">
                    <div className="grid gap-2">
                        <Label htmlFor="username">Username</Label>
                        <Input id="username" name="username" type="text" placeholder="someone" required />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" name="email" type="email"  placeholder="example@gmail.com" required />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="password">Password</Label>
                        <Input id="password" name="hashed_password" type="password" placeholder="keep it secret" required />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="balance">balance</Label>
                        <Input id="balance" name="balance" type="number" placeholder="no limit" required />
                    </div>
                </CardContent>


                <CardFooter className="flex flex-col gap-4">
                <Button type="submit" className="w-full">Create account</Button>
        <Button
            onClick={() => navigate("/login", { replace: true })}
            width="100%"
            colorScheme="gray"
            variant="outline"
            mt={6}
            className="w-full text-gray-500 border-gray-500">
            Login
          </Button>
      </CardFooter>
            </Card>
        </div>
    );
}

export default Register;
