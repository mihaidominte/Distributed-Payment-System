package com.client.paymentapp.tests

import org.json.JSONObject

object SendMoneyTest {

    fun sendMoney(amount: Double): String {
        val message = JSONObject().apply {
            put("activity", "send_money")
            put("id", 1)
            put("sender_id", 1)
            put("receiver_id", 2)
            put("password", "1234")
            put("amount", amount)
        }

        return message.toString() + "\n"
    }
}
