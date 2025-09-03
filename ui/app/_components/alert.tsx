import React from "react";
import {
  FaExclamationTriangle,
  FaTimesCircle,
  FaCheckCircle,
} from "react-icons/fa";

export interface AlertProps {
  type: "warning" | "danger" | "success";
  message: string;
}

const alertColors = {
  warning: "bg-yellow-500",
  danger: "bg-red-500",
  success: "bg-green-500",
};

export default function Alert({ type, message }: AlertProps) {
  return (
    <div
      className={`w-full p-4 flex items-center justify-center my-1 ${alertColors[type]}`}
    >
      {type === "warning" && (
        <FaExclamationTriangle className="text-white text-2xl mr-2" />
      )}
      {type === "danger" && (
        <FaTimesCircle className="text-white text-2xl mr-2" />
      )}
      {type === "success" && (
        <FaCheckCircle className="text-white text-2xl mr-2" />
      )}
      <span className="text-white">{message}</span>
    </div>
  );
}
