import { useEffect, useState } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faPlus } from "@fortawesome/free-solid-svg-icons";
import { faTrashAlt } from "@fortawesome/free-regular-svg-icons";
import { faGithub, faLinkedin, faTelegram } from "@fortawesome/free-brands-svg-icons";

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const [skills, setSkills] = useState([]);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await axios.get("http://127.0.0.1:8000/users/me", {
                    headers: { Authorization: `Bearer ${token}` },
                });

                setUser(response.data);
                setSkills(response.data.skills || []);
                setProjects(response.data.projects || []);
            } catch (error) {
                console.error("Failed to fetch user data", error);
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    return (
        <div className="grid grid-cols-6 gap-4 my-5 text-black">
            {/* Profile Section - Only Grows as Needed */}
            <div className="col-span-2 bg-white p-5 shadow-md rounded-md border border-green-700 flex flex-col self-start">
                <div className="flex flex-col items-center">
                    <img src="/pngimg.com - pokemon_PNG129.png" alt="Profile" className="mx-auto rounded-full w-32 h-32 object-cover border border-black" />
                </div>

                {loading ? (
                    <p className="text-gray-600 text-center mt-4">Loading profile...</p>
                ) : user ? (
                    <div className="mt-2">
                        <div className="text-center text-lg">
                            <p className="font-semibold">
                                {user.first_name} {user.last_name}
                            </p>
                            <p>{user.position || "Not specified"}</p>
                        </div>
                        <div className="mt-5">
                            <div className="flex justify-between">
                                <p>Location:</p>
                                <p>{user.city || "Not specified"}</p>
                            </div>
                        </div>

                        {/* Social Links - Conditionally Rendered */}
                        <div className="flex justify-center items-center space-x-5 mt-5">
                            {user.github && (
                                <a href={user.github} target="_blank" rel="noopener noreferrer">
                                    <FontAwesomeIcon icon={faGithub} size="xl" className="hover:text-green-700 transition" />
                                </a>
                            )}
                            {user.linkedin && (
                                <a href={user.linkedin} target="_blank" rel="noopener noreferrer">
                                    <FontAwesomeIcon icon={faLinkedin} size="xl" className="hover:text-green-700 transition" />
                                </a>
                            )}
                            {user.telegram && (
                                <a href={user.telegram.startsWith("http") ? user.telegram : `https://t.me/${user.telegram}`} target="_blank" rel="noopener noreferrer">
                                    <FontAwesomeIcon icon={faTelegram} size="xl" className="hover:text-green-700 transition" />
                                </a>
                            )}
                        </div>
                    </div>
                ) : (
                    <p className="text-gray-600 text-center mt-4">User data not available.</p>
                )}
                <div className="flex justify-center mt-5">
                    <button className="text-white bg-green-700 font-semibold px-3 shadow-md rounded-md cursor-pointer hover:bg-green-600">Edit profile</button>
                </div>
            </div>

            {/* Content Sections - Independent Growth */}
            <div className="col-span-4 col-start-3 flex flex-col space-y-4">
                {/* Projects Section */}
                <div className="bg-white border border-green-700 rounded-md shadow-md p-5 self-start w-full">
                    <p className="font-semibold text-lg">Projects</p>
                    {loading ? (
                        <p className="text-gray-600">Loading projects...</p>
                    ) : projects.length > 0 ? (
                        projects.map((project, index) => (
                            <div key={project.id} className="p-4 border-b last:border-b-0">
                                <h4 className="font-semibold">{project.name}</h4>
                                <p className="text-gray-600">{project.description}</p>
                                <button onClick={() => console.log(`Entered ${project.name}!`)} className="hover:text-green-700 transition duration-300 cursor-pointer underline">
                                    Enter Project
                                </button>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-700">No projects found.</p>
                    )}
                </div>

                {/* Skills Section */}
                <div className="bg-white border border-green-700 shadow-md rounded-md p-5 self-start w-full">
                    <div className="flex justify-between items-center mb-2">
                        <h3 className="font-semibold text-lg">Skills</h3>
                        <button className="border border-green-700 text-white bg-green-700 font-semibold px-2 shadow-md rounded-md cursor-pointer hover:bg-green-600">Add skill</button>
                    </div>
                    {loading ? (
                        <p className="text-gray-600">Loading skills...</p>
                    ) : skills.length > 0 ? (
                        skills.map((skill, index) => (
                            <div key={index} className="flex justify-between items-center px-4 py-2">
                                <p className="text-gray-700">{skill.name}</p>
                                <div className="flex space-x-2">
                                    <button className="hover:text-red-700">
                                        <FontAwesomeIcon icon={faTrashAlt} className="cursor-pointer" />
                                    </button>
                                    <button className="hover:text-green-700">
                                        <FontAwesomeIcon icon={faEdit} className="cursor-pointer" />
                                    </button>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-700">No skills added yet.</p>
                    )}
                </div>

                {/* Actions Section */}
                <div className="p-5 border border-green-700 rounded-md bg-white shadow-md self-start w-full">
                    <div className="flex justify-between items-center mb-2">
                        <h3 className="font-semibold text-lg">Actions</h3>
                        <button className="border border-green-700 text-white bg-green-700 font-semibold px-2 shadow-md rounded-md cursor-pointer hover:bg-green-600">New post</button>
                    </div>
                    <div>
                        <h4 className="font-semibold mb-2">Posts</h4>
                        <ul>
                            <li className="mb-2">
                                <div className="bg-white p-4 shadow-md">
                                    <h5 className="font-semibold">Blog Post Title 1</h5>
                                    <p className="text-gray-600">Excerpt of blog post content...</p>
                                </div>
                            </li>
                            <li className="mb-2">
                                <div className="bg-white p-4 shadow-md">
                                    <h5 className="font-semibold">Blog Post Title 2</h5>
                                    <p className="text-gray-600">Excerpt of blog post content...</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
