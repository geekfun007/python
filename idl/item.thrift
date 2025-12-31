/**
 * 物品服务 IDL 定义
 * Item Service Interface Definition
 */

namespace py app.thrift_gen.item

include "common.thrift"
include "user.thrift"

/**
 * 物品状态枚举
 */
enum ItemStatus {
    DRAFT = 0,          // 草稿
    PENDING = 1,        // 待审核
    ACTIVE = 2,         // 已上架
    INACTIVE = 3,       // 已下架
    SOLD_OUT = 4,       // 已售罄
    DELETED = 5,        // 已删除
}

/**
 * 物品分类枚举
 */
enum ItemCategory {
    OTHER = 0,          // 其他
    ELECTRONICS = 1,    // 电子产品
    CLOTHING = 2,       // 服装
    FOOD = 3,           // 食品
    BOOKS = 4,          // 图书
    HOME = 5,           // 家居
    SPORTS = 6,         // 运动
    BEAUTY = 7,         // 美妆
    TOYS = 8,           // 玩具
}

// ============================================
// 数据传输对象 (DTO)
// ============================================

/**
 * 价格信息
 */
struct PriceInfo {
    1: required double price,               // 当前价格
    2: optional double original_price,      // 原价
    3: optional double discount,            // 折扣率 (0-1)
    4: required string currency,            // 货币代码 (CNY, USD等)
}

/**
 * 库存信息
 */
struct StockInfo {
    1: required i32 stock,                  // 当前库存
    2: optional i32 sold_count,             // 已售数量
    3: optional i32 reserved_count,         // 预留数量
}

/**
 * 物品基础信息
 */
struct ItemInfo {
    1: required i64 id,                     // 物品ID
    2: required string title,               // 标题
    3: optional string description,         // 描述
    4: required PriceInfo price_info,       // 价格信息
    5: required ItemCategory category,      // 分类
    6: required ItemStatus status,          // 状态
    7: required StockInfo stock_info,       // 库存信息
    8: required i64 owner_id,               // 所有者ID
    9: optional string owner_name,          // 所有者名称
    10: optional list<string> images,       // 图片URL列表
    11: optional list<string> tags,         // 标签列表
    12: required i64 created_at,            // 创建时间戳
    13: required i64 updated_at,            // 更新时间戳
}

/**
 * 物品详情（包含更多信息）
 */
struct ItemDetail {
    1: required ItemInfo base_info,         // 基础信息
    2: optional string content,             // 详情内容（富文本）
    3: optional map<string, string> attributes, // 属性键值对
    4: optional i64 view_count,             // 浏览次数
    5: optional i64 favorite_count,         // 收藏次数
    6: optional user.UserInfo owner,        // 所有者信息
}

// ============================================
// 请求/响应结构
// ============================================

/**
 * 创建物品请求
 */
struct CreateItemRequest {
    1: required string title,               // 标题 (1-200字符)
    2: optional string description,         // 描述 (最多2000字符)
    3: required double price,               // 价格
    4: optional double original_price,      // 原价
    5: required ItemCategory category,      // 分类
    6: optional i32 stock,                  // 库存数量
    7: optional list<string> images,        // 图片URL列表
    8: optional list<string> tags,          // 标签列表
    9: optional string content,             // 详情内容
    10: optional map<string, string> attributes, // 属性
}

/**
 * 创建物品响应
 */
struct CreateItemResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional ItemInfo item,              // 创建的物品信息
}

/**
 * 获取物品请求
 */
struct GetItemRequest {
    1: required i64 item_id,                // 物品ID
    2: optional bool with_owner,            // 是否包含所有者信息
}

/**
 * 获取物品响应
 */
struct GetItemResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional ItemDetail item,            // 物品详情
}

/**
 * 获取物品列表请求
 */
struct ListItemsRequest {
    1: required common.PaginationRequest pagination, // 分页参数
    2: optional ItemCategory category,               // 分类过滤
    3: optional ItemStatus status,                   // 状态过滤
    4: optional double min_price,                    // 最低价格
    5: optional double max_price,                    // 最高价格
    6: optional i64 owner_id,                        // 所有者ID
    7: optional string search,                       // 搜索关键词
    8: optional list<string> tags,                   // 标签过滤
    9: optional common.TimeRange time_range,         // 时间范围
}

/**
 * 获取物品列表响应
 */
struct ListItemsResponse {
    1: required common.BaseResponse base,            // 基础响应
    2: optional list<ItemInfo> items,                // 物品列表
    3: optional common.PaginationInfo pagination,    // 分页信息
}

/**
 * 更新物品请求
 */
struct UpdateItemRequest {
    1: required i64 item_id,                // 物品ID
    2: optional string title,               // 新标题
    3: optional string description,         // 新描述
    4: optional double price,               // 新价格
    5: optional double original_price,      // 新原价
    6: optional ItemCategory category,      // 新分类
    7: optional ItemStatus status,          // 新状态
    8: optional i32 stock,                  // 新库存
    9: optional list<string> images,        // 新图片列表
    10: optional list<string> tags,         // 新标签列表
    11: optional string content,            // 新详情内容
    12: optional map<string, string> attributes, // 新属性
}

/**
 * 更新物品响应
 */
struct UpdateItemResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional ItemInfo item,              // 更新后的物品信息
}

/**
 * 删除物品请求
 */
struct DeleteItemRequest {
    1: required i64 item_id,                // 物品ID
    2: optional bool hard_delete,           // 是否硬删除
}

/**
 * 删除物品响应
 */
struct DeleteItemResponse {
    1: required common.BaseResponse base,   // 基础响应
}

/**
 * 更新物品状态请求
 */
struct UpdateItemStatusRequest {
    1: required i64 item_id,                // 物品ID
    2: required ItemStatus status,          // 新状态
    3: optional string reason,              // 变更原因
}

/**
 * 更新物品状态响应
 */
struct UpdateItemStatusResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional ItemInfo item,              // 更新后的物品信息
}

/**
 * 更新库存请求
 */
struct UpdateStockRequest {
    1: required i64 item_id,                // 物品ID
    2: required i32 quantity,               // 变化量（正数增加，负数减少）
    3: optional string reason,              // 变更原因
}

/**
 * 更新库存响应
 */
struct UpdateStockResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional StockInfo stock_info,       // 更新后的库存信息
}

/**
 * 批量获取物品请求
 */
struct BatchGetItemsRequest {
    1: required list<i64> item_ids,         // 物品ID列表
}

/**
 * 批量获取物品响应
 */
struct BatchGetItemsResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional map<i64, ItemInfo> items,   // 物品ID -> 物品信息映射
}

// ============================================
// 服务接口定义
// ============================================

/**
 * 物品服务接口
 */
service ItemService {
    /**
     * 创建物品
     */
    CreateItemResponse CreateItem(1: CreateItemRequest request),
    
    /**
     * 获取物品详情
     */
    GetItemResponse GetItem(1: GetItemRequest request),
    
    /**
     * 获取物品列表
     */
    ListItemsResponse ListItems(1: ListItemsRequest request),
    
    /**
     * 更新物品
     */
    UpdateItemResponse UpdateItem(1: UpdateItemRequest request),
    
    /**
     * 删除物品
     */
    DeleteItemResponse DeleteItem(1: DeleteItemRequest request),
    
    /**
     * 更新物品状态（上架/下架）
     */
    UpdateItemStatusResponse UpdateItemStatus(1: UpdateItemStatusRequest request),
    
    /**
     * 更新库存
     */
    UpdateStockResponse UpdateStock(1: UpdateStockRequest request),
    
    /**
     * 批量获取物品
     */
    BatchGetItemsResponse BatchGetItems(1: BatchGetItemsRequest request),
}
