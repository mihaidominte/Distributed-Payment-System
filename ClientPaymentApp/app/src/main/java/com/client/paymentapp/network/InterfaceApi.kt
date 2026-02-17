package com.client.paymentapp.network

import retrofit2.http.Body
import retrofit2.http.POST

interface InterfaceApi {
    @POST("/users/start-config")
    suspend fun startConfig(
        @Body request: StartConfigRequest
    ): StartConfigResponse

    @POST("/users/final-config")
    suspend fun finalizeConfig(
        @Body request: FinalizeConfigRequest
    ): GenericResponse
}