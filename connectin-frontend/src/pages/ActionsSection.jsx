import { useState, useEffect } from "react";
import axios from "axios";
import { NavLink } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { toast } from "react-toastify";

const ActionsSection = ({ user, posts: propPosts, loading, isStatic }) => {
    const [posts, setPosts] = useState([]);
    const [localLoading, setLocalLoading] = useState(true);

    useEffect(() => {
        if (isStatic && propPosts) {
            setPosts(propPosts);
            setLocalLoading(false);
            return;
        }

        fetchPosts();
    }, [isStatic, propPosts]);

    const fetchPosts = async () => {
        try {
            setLocalLoading(true);
            const token = localStorage.getItem("access_token");
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/posts/my`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (response?.data) {
                setPosts(response.data);
            }
        } catch (error) {
            console.error("Failed to fetch posts:", error);
            toast.error("Failed to load posts");
        } finally {
            setLocalLoading(false);
        }
    };

    const handleDeletePost = async (postId) => {
        if (!window.confirm("Are you sure you want to delete this post?")) return;

        try {
            const token = localStorage.getItem("access_token");
            await axios.delete(`${import.meta.env.VITE_API_URL}/posts/${postId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            toast.success("Post deleted successfully");
            setPosts((prev) => prev.filter((post) => post.id !== postId));
        } catch (error) {
            console.error("Failed to delete post:", error);
            toast.error("Failed to delete post");
        }
    };

    return (
        <div className="space-y-6">
            {loading || localLoading ? (
                <p className="text-center text-gray-500 py-4">Loading posts...</p>
            ) : posts && posts.length > 0 ? (
                <div className="space-y-4">
                    {posts.map((post) => (
                        <div key={post.id} className="border border-gray-200 rounded-md p-4 hover:shadow-md transition">
                            <div className="flex justify-between items-start">
                                <div className="flex-1">
                                    <h3 className="font-semibold text-lg mb-2">{post.title}</h3>
                                    {post.tags?.length > 0 && (
                                        <div className="flex flex-wrap gap-2 mb-3">
                                            {post.tags.map((tag) => (
                                                <span key={`${post.id}-${tag.id || tag}`} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-md">
                                                    {tag.name || tag}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                    <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: post.content }} />
                                </div>
                                <div className="flex items-center space-x-2 ml-4">
                                    {user && user.id === post.author?.id && (
                                        <button
                                            onClick={() => handleDeletePost(post.id)}
                                            className="text-red-500 hover:text-red-700 px-2 py-1 flex items-center gap-2"
                                        >
                                            <FontAwesomeIcon icon={faTrashAlt} />
                                            Delete
                                        </button>
                                    )}
                                    <NavLink to={`/post/${post.id}`} className="bg-green-700 text-white px-3 py-1 rounded hover:bg-green-600">
                                        View
                                    </NavLink>
                                </div>
                            </div>

                            <div className="flex mt-4 text-sm text-gray-500">
                                <div className="flex items-center mr-4">
                                    <span>Likes: {post.likes_count}</span>
                                </div>
                                <div className="flex items-center">
                                    <span>Comments: {post.comments_count}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-8 border border-dashed rounded-md">
                    <p className="text-gray-500">No posts available.</p>
                    <NavLink to="/post" className="text-green-700 hover:underline mt-2 inline-block">
                        Create your first post
                    </NavLink>
                </div>
            )}
        </div>
    );
};

export default ActionsSection;
