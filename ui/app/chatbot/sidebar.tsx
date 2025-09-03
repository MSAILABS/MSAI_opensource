import React, { useEffect, useRef, useState } from "react";

import axios from "axios";

import config from "@/utilities/config";
import Alert, { AlertProps } from "../_components/alert";
import Loading from "../_components/loading";

interface SidebarParams {
  enableChat: boolean;
  setEnableChat: any;
  selectedGroup: any;
  setSelectedGroup: any;
}

const Sidebar: React.FC<SidebarParams> = ({
  enableChat,
  setEnableChat,
  selectedGroup,
  setSelectedGroup,
}) => {
  const [loading, setLoading] = useState("");
  const [alertState, setAlertState] = useState<AlertProps>({
    type: "danger",
    message: "",
  });

  const [clusters, setClusters] = useState([]);

  const clusterNameInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (clusters && clusters.length > 0 && selectedGroup != null) {
      setEnableChat(true);
    } else {
      setEnableChat(false);
    }

    localStorage.setItem("selectedGroup", JSON.stringify(selectedGroup));
  }, [clusters, selectedGroup]);

  useEffect(() => {
    get_clusters();
  }, []);

  const updateAlertState = ({ type, message }: AlertProps) => {
    setAlertState({
      type: type,
      message: message,
    });

    setTimeout(() => {
      setAlertState((prev) => ({ ...prev, message: "" }));
    }, 5000);
  };

  const get_clusters = async () => {
    try {
      setLoading("Getting all groups");
      const res = await axios.get(`${config.api_url}/get_clusters`);

      if (res) {
        if (res.data?.clusters.length > 0) {
          setClusters(res.data?.clusters);
        } else {
          updateAlertState({
            type: "warning",
            message: "No groups found, please add one.",
          });
          setClusters([]);
        }
      } else {
        updateAlertState({ type: "danger", message: "Couldn't get groups" });
      }
    } catch (err) {
      console.log(err);
      updateAlertState({ type: "danger", message: "Couldn't get groups" });
    } finally {
      setLoading("");
    }
  };

  const add_new_cluster = async () => {
    const value = clusterNameInputRef.current?.value || "";
    const valid = /^[a-zA-Z0-9 _]+$/.test(value);
    if (!value.trim()) {
      alert("Name cannot be empty.");
      return;
    }
    if (!valid) {
      alert("Name can only contain alphabets, numbers, _ and spaces.");
      return;
    }

    setLoading("Adding new group");

    try {
      const res = await axios.post(
        `${config.api_url}/add_cluster`,
        {},
        {
          params: {
            cluster_name: value.trim(),
          },
        }
      );

      if (res) {
        if (res.data?.message) {
          updateAlertState({ type: "success", message: "Group created" });

          get_clusters();
        } else {
          updateAlertState({
            type: "danger",
            message: "Couldn't create group",
          });
        }
      }
    } catch (err) {
      updateAlertState({ type: "danger", message: "Something went wrong!!!" });
    } finally {
      setLoading("");
      if (clusterNameInputRef.current) {
        clusterNameInputRef.current.value = "";
      }
    }
  };

  const delete_cluster = async (id: number) => {
    setLoading("Deleting Group");
    try {
      const res = await axios.delete(`${config.api_url}/delete_cluster`, {
        params: { cluster_id: id },
      });

      console.log(res);

      if (res) {
        if (res.data?.message) {
          updateAlertState({ type: "success", message: "Group deleted" });
          get_clusters();
        } else {
          updateAlertState({
            type: "danger",
            message: "Couldn't delete group",
          });
        }
      }
    } catch (err) {
      updateAlertState({
        type: "danger",
        message: "Couldn't delete group",
      });
    } finally {
      setLoading("");
      setSelectedGroup(null);
    }
  };

  return (
    <div style={{ width: "100%" }}>
      <h1 className="mt-5 mb-9" style={{ fontSize: "2em" }}>
        Groups
      </h1>
      <div className="grid mb-4" style={{ gridTemplateColumns: "auto 80px" }}>
        <input
          type="text"
          placeholder="Name"
          className="chat-text-area w-full"
          ref={clusterNameInputRef}
        />
        <button
          className="chat-buttons-right bg-white text-black"
          style={{
            width: "80px",
            borderRadius: "5px",
            justifyContent: "center",
          }}
          onClick={add_new_cluster}
        >
          Create
        </button>
      </div>
      {loading != "" && <Loading message={loading} textSizeClass="text-m" />}
      {alertState.message != "" && (
        <Alert type={alertState.type} message={alertState.message} />
      )}
      <div className="grid">
        {clusters &&
          clusters.length > 0 &&
          clusters.map((cluster, index) => (
            <div
              key={index}
              className={
                "grid p-2 my-2 rounded-[10px] border border-gray-400 items-center cursor-pointer hover:bg-gray-200 hover:text-black" +
                (selectedGroup && selectedGroup["id"] == cluster["id"]
                  ? " bg-blue-500"
                  : "")
              }
              style={{
                gridTemplateColumns: "auto 30px",
                gap: "10px",
              }}
              onClick={() =>
                setSelectedGroup({ name: cluster["name"], id: cluster["id"] })
              }
            >
              <p>{cluster["name"]}</p>
              <button
                className="bg-red-500 w-[30px] h-[30px] rounded-[5px] text-[20px] flex items-center justify-center"
                onClick={() => delete_cluster(cluster["id"])}
              >
                🗑
              </button>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Sidebar;
