/**
 * User Service Thrift Definition
 * 用户服务 Thrift 定义
 */

namespace py user_service

include "common.thrift"

/**
 * 用户信息结构
 */
struct UserInfo {
    1: required i32 id,
    2: required string username,
    3: required string email,
    4: optional string full_name,
    5: optional i32 age,
    6: required bool is_active,
    7: optional bool is_superuser,
    8: optional string created_at,
    9: optional string updated_at
}

/**
 * 创建用户请求
 */
struct CreateUserRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string full_name,
    5: optional i32 age
}

/**
 * 更新用户请求
 */
struct UpdateUserRequest {
    1: optional string full_name,
    2: optional i32 age,
    3: optional string password,
    4: optional bool is_active
}

/**
 * 用户列表响应
 */
struct UserListResponse {
    1: required i32 total,
    2: required list<UserInfo> items
}

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 创建用户
     */
    UserInfo createUser(1: CreateUserRequest request) throws (1: common.ServiceException ex),
    
    /**
     * 获取用户详情
     */
    UserInfo getUser(1: i32 user_id) throws (1: common.ServiceException ex),
    
    /**
     * 获取用户列表
     */
    UserListResponse listUsers(1: common.PaginationParams params) throws (1: common.ServiceException ex),
    
    /**
     * 更新用户
     */
    UserInfo updateUser(1: i32 user_id, 2: UpdateUserRequest request) throws (1: common.ServiceException ex),
    
    /**
     * 删除用户
     */
    bool deleteUser(1: i32 user_id) throws (1: common.ServiceException ex),
    
    /**
     * 根据用户名搜索
     */
    UserListResponse searchUsersByName(1: string search_term, 2: common.PaginationParams params) throws (1: common.ServiceException ex),
    
    /**
     * 根据用户名获取用户
     */
    UserInfo getUserByUsername(1: string username) throws (1: common.ServiceException ex)
}
