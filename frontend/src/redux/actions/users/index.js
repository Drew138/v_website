import axios from "axios"
import { UPDATE_USER_PROFILE_ENDPOINT } from "../../../config"

export const setUser = (user) => {
  return dispatch => {
    dispatch({
      type: "SELECT_USER_FOR_UPDATE",
      payload: user
    })
  }
}

// export const setUsersList = (users) => {
//     return dispatch => {
//         dispatch({
//             type: "SET_USERS_LIST",
//             payload: users
//         })
//     }
// }

export const updateUser = (user) => {
  return async dispatch => {

    try {
      const data = new FormData();
      for (const [key, value] of Object.entries(user)) {
        if (value && value !== "N/A") {
          if (key === "selectedFile") {
            data.append("picture", value)
          } else {
            // console.log(key)
            data.append(key, value)
          }
        }
      }
      const res = await axios.patch(
        `${UPDATE_USER_PROFILE_ENDPOINT}${user.id}/`, data)
      dispatch({
        type: "UPDATE_USER",
        payload: { ...res.data }
      })
      const alertData = {
        title: "Información de Usuario Actualizada Exitosamente",
        success: true,
        show: true,
        alertText: `Se Ha Actualizado Exitosamente la Información de ${res.data.first_name} ${res.data.last_name}`
      }
      dispatch({
        type: "DISPLAY_SWEET_ALERT",
        payload: alertData
      })
    } catch (e) {
      const alerData = {
        title: "Error de Validación",
        success: false,
        show: true,
        alertText: Object.entries(e.response.data)[0][1][0]
      }
      dispatch({
        type: "DISPLAY_SWEET_ALERT",
        payload: alerData
      })
    }
  }
}