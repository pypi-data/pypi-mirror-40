namespace java com.didapinche.thrift.dm.hub.holder

struct Result{
	1:i32 code,
	2:string msg
}

struct DeviceResult{
	1:i32 code,
	2:string userids
}


service DmOperationHubService{
	void holdOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
	Result holdOrderBatch(1:list<i64> OrderIds,2:i32 sysOpId,3:string content)
    
	void cancelHoldOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
	
    Result holdTaxiOrder(1:i64 OrderId,2:i32 sysOpId,3:string content,4:bool isSend)
	Result holdTaxiOrderBatch(1:list<i64> OrderIds,2:i32 sysOpId,3:string content,4:bool isSend)

	Result cancelHoldTaxiOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
    
	Result forbiddenUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result forbiddenUserBatch(1:list<i64> userIds,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
    
    Result getUserIdByReference(1:string reference)
    
	Result unforbiddenUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result forbiddenDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:byte group_id)
	DeviceResult forbiddenDevice(1:string deviceId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	DeviceResult unforbiddenDevice(1:string deviceId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result forbiddenPost(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenPost(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result taxiOrderSetTag(1:i64 taxi_order_id,2:byte group_id,3:string reason,4:i64 sys_op_id,5:string sys_op_ip)
	Result delReply(1:string replyId)
	Result delReplyMulti(1:string replyIds)
	Result maskReply(1:string replyId,2:byte mask)
	Result maskReplyMulti(1:string replyIds)
	Result forbiddenTaxiUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenTaxiUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result forbiddenTaxiDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenTaxiDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:byte group_id)
	Result userOrderSetTag(1:i64 order_id,2:byte group_id,3:string reason,4:i64 sys_op_id,5:string sys_op_ip)
	Result taxiOrderSetTagAndDebit(1:i64 taxi_order_id, 2:string debitContent, 3:i64 sys_op_id, 4:i32 debitType, 5:string debitMoney)
	Result addWhiteDevice(1:string devicecid)
	Result removeWhiteDevice(1:string devicecid)
	 // 修改用户账户提现状态
    Result updateWithdrawState(1:i64 user_id, 2:string type, 3:byte state, 4:string remark, 5:i32 sys_op_id, 6:string sys_op_ip);
    
    // order_id参数为字符串
    Result holdTaxiOrderString(1:string OrderId,2:i32 sysOpId,3:string content,4:bool isSend)
}