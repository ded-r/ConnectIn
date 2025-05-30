import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUp, faArrowDown, faUser, faLink } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-regular-svg-icons";
import { NavLink } from "react-router";
import { toast } from "react-toastify";
import { useNavigate } from "react-router";
import useProjectVoteStore from "../../store/projectVoteStore";

const ProjectCard = ({ project, currentUser, handleApply, showViewProject = true, showCommentsLink = false, isLoading = false, showFullContent = false }) => {
    const [isVoteLoading, setIsVoteLoading] = useState(false);
    const [isApplyLoading, setIsApplyLoading] = useState(false);
    const [isCopyLoading, setIsCopyLoading] = useState(false);
    const navigate = useNavigate();
    const { voteProject, getVoteStatus, initializeVoteState } = useProjectVoteStore();
    const { hasVoted, isUpvote, voteCount } = getVoteStatus(project.id);

    useEffect(() => {
        // Initialize vote state when component mounts
        const token = localStorage.getItem("access_token");
        if (token) {
            initializeVoteState([project.id]);
        }
    }, [project.id, initializeVoteState]);

    const handleOwnerClick = (e) => {
        e.stopPropagation(); // Prevent card click propagation
        if (owner && owner.id) {
            navigate(`/profile/${owner.id}`);
        }
    };

    const handleVote = async (isUpvote) => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            toast.error("Please log in to vote");
            navigate("/login", { state: { from: window.location.pathname } });
            return;
        }

        setIsVoteLoading(true);
        try {
            await voteProject(project.id, isUpvote);
        } catch (error) {
            console.error("Failed to vote:", error);
            toast.error("Failed to vote. Please try again.");
        } finally {
            setIsVoteLoading(false);
        }
    };

    const handleApplyClick = async (e) => {
        if (e) e.stopPropagation(); // Prevent click propagation if event exists
        
        const token = localStorage.getItem("access_token");
        if (!token) {
            toast.error("Please log in to apply");
            navigate("/login", { state: { from: window.location.pathname } });
            return;
        }

        setIsApplyLoading(true);
        try {
            const response = await handleApply(project.id);
            // Only show success toast if there's no error response
            if (!response || !response.error) {
                toast.success("Application submitted successfully!");
            }
        } catch (error) {
            console.error("Failed to apply:", error);
            // Display the specific error message from the backend
            const errorMessage = error.response?.data?.detail || "Failed to apply. Please try again.";
            toast.error(errorMessage);
        } finally {
            setIsApplyLoading(false);
        }
    };

    const handleCopyLink = async (e) => {
        if (e) e.stopPropagation(); // Prevent click propagation if event exists
        
        setIsCopyLoading(true);
        try {
            const url = `${window.location.origin}/feed/project/${project.id}`;
            await navigator.clipboard.writeText(url);
            toast.success("Project link copied to clipboard!");
        } catch (error) {
            toast.error("Failed to copy link");
            console.error("Copy failed:", error);
        } finally {
            setIsCopyLoading(false);
        }
    };

    const owner = project.owner || {
        avatar_url: "https://cdn-icons-png.flaticon.com/512/149/149071.png",
        username: "Unknown",
        id: null,
    };

    return (
        <div className={`bg-white dark:bg-gray-800 shadow-md rounded-md border border-green-700 p-5 hover:shadow-lg transition-shadow relative ${isLoading ? 'pointer-events-none' : ''}`}>
            <div className="flex items-center space-x-2 mb-4">
                <div 
                    onClick={handleOwnerClick}
                    className="relative w-10 h-10 flex items-center justify-center rounded-full border-2 border-green-700 dark:border-green-500 bg-gray-100 dark:bg-gray-700 cursor-pointer hover:opacity-90 transition-opacity"
                >
                    {owner.avatar_url ? (
                        <img
                            src={owner.avatar_url}
                            alt={owner.username}
                            className="w-full h-full rounded-full object-cover"
                            onError={(e) => {
                                e.target.src = "";
                                e.target.onerror = null;
                            }}
                        />
                    ) : (
                        <FontAwesomeIcon icon={faUser} className="text-gray-500 dark:text-gray-400" />
                    )}
                </div>
                <div>
                    <p 
                        onClick={handleOwnerClick}
                        className="font-semibold cursor-pointer hover:text-green-700 dark:hover:text-green-500 transition-colors"
                    >
                        {owner.username}
                    </p>
                </div>
            </div>

            {project.tags?.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                    {project.tags.map((tag) => (
                        <span key={tag.id} className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded-full">
                            {tag.name}
                        </span>
                    ))}
                </div>
            )}

            <h3 className="text-lg font-bold mb-2">{project.name || "Untitled Project"}</h3>
            <p className={`text-sm text-gray-700 dark:text-gray-300 mb-3 ${!showFullContent ? 'line-clamp-6 overflow-hidden' : ''}`} dangerouslySetInnerHTML={{ __html: project.description || "No description available." }} />

            <div className="mt-3 flex flex-wrap gap-2 mb-4">
                {project.skills?.length > 0 ? (
                    project.skills.map((skill) => (
                        <span key={skill.id} className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100 rounded-md">
                            {skill.name}
                        </span>
                    ))
                ) : (
                    <span className="text-gray-500 text-xs">No skills</span>
                )}
            </div>

            <div className="flex justify-between items-center mt-3">
                <div className="space-x-3">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            handleVote(true);
                        }}
                        disabled={isVoteLoading}
                        className={`group relative transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${hasVoted && isUpvote ? "text-green-700" : "text-gray-500 hover:text-green-700"}`}
                        title={isVoteLoading ? "Processing..." : "Upvote"}
                    >
                        <FontAwesomeIcon icon={faArrowUp} className={`${isVoteLoading ? "animate-pulse" : ""}`} />
                        <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{hasVoted && isUpvote ? "Remove upvote" : "Upvote"}</span>
                    </button>
                    <span className="text-gray-700 dark:text-gray-300 font-bold">{voteCount}</span>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            handleVote(false);
                        }}
                        disabled={isVoteLoading}
                        className={`group relative transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${hasVoted && !isUpvote ? "text-red-700" : "text-gray-500 hover:text-red-700"}`}
                        title={isVoteLoading ? "Processing..." : "Downvote"}
                    >
                        <FontAwesomeIcon icon={faArrowDown} className={`${isVoteLoading ? "animate-pulse" : ""}`} />
                        <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{hasVoted && !isUpvote ? "Remove downvote" : "Downvote"}</span>
                    </button>
                    {showCommentsLink && (
                        <NavLink 
                            to={`/feed/project/${project.id}`} 
                            onClick={(e) => e.stopPropagation()}
                            className="group relative text-gray-500 hover:text-blue-700 transition cursor-pointer" 
                            title="View comments"
                        >
                            <FontAwesomeIcon icon={faComment} />
                            <span className="ml-1">{project.comments_count || ""}</span>
                            <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Comments</span>
                        </NavLink>
                    )}
                    <button
                        onClick={(e) => handleCopyLink(e)}
                        disabled={isCopyLoading}
                        className="group relative text-gray-500 hover:text-blue-500 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        title={isCopyLoading ? "Copying..." : "Copy link"}
                    >
                        <FontAwesomeIcon icon={faLink} className={`${isCopyLoading ? "animate-pulse" : ""}`} />
                        <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Copy link</span>
                    </button>
                </div>

                <div className="space-x-3">
                    {currentUser && currentUser.id !== owner.id && (
                        <button
                            onClick={(e) => handleApplyClick(e)}
                            disabled={isApplyLoading}
                            className="rounded shadow-sm text-sm px-6 py-2 border border-green-700 hover:text-white font-semibold cursor-pointer hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                            title={isApplyLoading ? "Processing..." : "Apply to project"}
                        >
                            {isApplyLoading ? "Applying..." : "Apply"}
                        </button>
                    )}
                    {showViewProject && (
                        <NavLink 
                            to={`/feed/project/${project.id}`} 
                            onClick={(e) => e.stopPropagation()}
                            className="rounded shadow-sm text-sm px-6 py-2 border border-green-700 hover:text-white font-semibold cursor-pointer hover:bg-green-700 transition" 
                            title="View project details"
                        >
                            View Project
                        </NavLink>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProjectCard;
