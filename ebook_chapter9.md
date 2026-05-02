# Chapter 9: Income Maximization

## Scaling Your Revenue Streams

You've built a successful product and automated your business. Now it's time to maximize your income. In this chapter, you'll learn advanced pricing strategies, upsell techniques, customer lifetime value optimization, and business model diversification to take your earnings to the next level.

## Advanced Pricing Strategies

### Value-Based Pricing Framework

**The 5-Level Pricing Model:**
```
Level 1: Cost-Plus ($27-$97)
  - Covers costs plus small profit
  - Entry-level positioning
  - High volume potential

Level 2: Market-Competitive ($97-$197)
  - Matches competitor pricing
  - Standard features
  - Main revenue stream

Level 3: Value-Based ($197-$497)
  - Based on perceived value
  - Premium features
  - Higher margins

Level 4: Transformational ($497-$997)
  - Life-changing results
  - Comprehensive solutions
  - Premium positioning

Level 5: Enterprise ($997+)
  - Custom solutions
  - White-label options
  - Corporate clients
```

**Implementing Tiered Pricing:**
```javascript
// Dynamic pricing engine
class PricingEngine {
    constructor() {
        this.tiers = {
            basic: {
                price: 97,
                features: [
                    'Ebook PDF',
                    'Basic templates',
                    'Email support',
                    '30-day updates'
                ],
                position: 'entry'
            },
            pro: {
                price: 197,
                features: [
                    'Everything in Basic',
                    'Video tutorials',
                    'Advanced templates',
                    'Priority support',
                    '1-year updates',
                    'Community access'
                ],
                position: 'main'
            },
            premium: {
                price: 497,
                features: [
                    'Everything in Pro',
                    '1-on-1 coaching session',
                    'Custom templates',
                    'Lifetime updates',
                    'Private mastermind',
                    'Early access to new features'
                ],
                position: 'premium'
            }
        };
        
        this.discounts = {
            launch: 0.3,    // 30% launch discount
            bundle: 0.2,    // 20% bundle discount
            annual: 0.17,   // 2 months free for annual
            loyalty: 0.1    // 10% loyalty discount
        };
    }
    
    calculatePrice(tier, options = {}) {
        let basePrice = this.tiers[tier].price;
        
        // Apply discounts
        if (options.discount) {
            basePrice *= (1 - this.discounts[options.discount]);
        }
        
        // Apply bundle pricing
        if (options.bundle) {
            basePrice *= (1 - this.discounts.bundle);
        }
        
        // Apply payment term discount
        if (options.paymentTerm === 'annual') {
            basePrice *= (1 - this.discounts.annual);
        }
        
        // Round to nearest dollar
        return Math.round(basePrice);
    }
    
    getTierComparison() {
        return Object.entries(this.tiers).map(([name, tier]) => ({
            name,
            price: tier.price,
            features: tier.features,
            valueScore: this.calculateValueScore(tier),
            recommended: this.isRecommendedTier(name)
        }));
    }
    
    calculateValueScore(tier) {
        // Calculate value per dollar
        const featureCount = tier.features.length;
        const valuePerDollar = featureCount / tier.price;
        
        // Adjust for premium features
        const premiumMultiplier = tier.position === 'premium' ? 1.5 : 1;
        
        return (valuePerDollar * 100 * premiumMultiplier).toFixed(1);
    }
    
    isRecommendedTier(tierName) {
        // Recommend Pro tier as best value
        return tierName === 'pro';
    }
    
    // Dynamic pricing based on demand
    adjustPriceForDemand(tier, demandLevel) {
        const basePrice = this.tiers[tier].price;
        
        switch(demandLevel) {
            case 'low':
                return basePrice * 0.9;  // 10% discount
            case 'normal':
                return basePrice;
            case 'high':
                return basePrice * 1.1;  // 10% premium
            case 'very-high':
                return basePrice * 1.25; // 25% premium
            default:
                return basePrice;
        }
    }
}

// Usage example
const pricing = new PricingEngine();

// Calculate price with launch discount
const launchPrice = pricing.calculatePrice('pro', { discount: 'launch' });
console.log(`Launch price: $${launchPrice}`);

// Get tier comparison
const comparison = pricing.getTierComparison();
console.log('Tier comparison:', comparison);
```

### Psychological Pricing Techniques

**Price Anchoring Implementation:**
```javascript
// Price anchoring system
class PriceAnchoring {
    constructor() {
        this.anchors = {
            decoy: {
                name: 'Professional Package',
                price: 297,
                features: [
                    'Ebook PDF',
                    'Basic templates',
                    'Email support'
                ],
                purpose: 'make_pro_look_better'
            },
            pro: {
                name: 'Pro Package',
                price: 197,
                features: [
                    'Ebook PDF',
                    'All templates',
                    'Priority support',
                    'Video tutorials',
                    'Community access'
                ],
                purpose: 'target_sale'
            },
            premium: {
                name: 'Premium Package',
                price: 497,
                features: [
                    'Everything in Pro',
                    '1-on-1 coaching',
                    'Custom templates',
                    'Lifetime updates'
                ],
                purpose: 'increase_perceived_value'
            }
        };
    }
    
    displayPricingPage() {
        const packages = Object.values(this.anchors);
        
        // Sort by price
        packages.sort((a, b) => a.price - b.price);
        
        // Calculate value indicators
        packages.forEach(pkg => {
            pkg.valuePerDollar = pkg.features.length / pkg.price;
            pkg.popular = pkg.purpose === 'target_sale';
            pkg.bestValue = this.calculateBestValue(packages, pkg);
        });
        
        return packages;
    }
    
    calculateBestValue(packages, currentPackage) {
        // The middle package is usually perceived as best value
        const middleIndex = Math.floor(packages.length / 2);
        return packages.indexOf(currentPackage) === middleIndex;
    }
    
    // Charm pricing (ending in 7, 9, or 97)
    applyCharmPricing(price) {
        const endings = [97, 99, 97];
        const base = Math.floor(price / 100) * 100;
        const ending = endings[Math.floor(Math.random() * endings.length)];
        return base + ending;
    }
    
    // Tier highlighting
    highlightRecommendedTier(tiers) {
        return tiers.map(tier => ({
            ...tier,
            highlighted: tier.popular,
            badge: tier.popular ? 'MOST POPULAR' : null,
            emphasis: tier.bestValue ? 'BEST VALUE' : null
        }));
    }
}
```

## Upsell & Cross-Sell Systems

### Automated Upsell Engine

**Post-Purchase Upsell Flow:**
```javascript
class UpsellEngine {
    constructor() {
        this.upsellOffers = {
            immediate: {
                name: 'Fast Action Bonus',
                description: 'Get our premium templates for 50% off if you act now!',
                price: 47,  // Normally $97
                discount: 0.5,
                timeframe: 15, // minutes
                conditions: ['immediate_post_purchase'],
                conversionRate: 0.35  // 35% conversion expected
            },
            one_click: {
                name: 'One-Click Upgrade',
                description: 'Upgrade to Pro for just $100 more',
                price: 100,
                originalPrice: 200,
                conditions: ['basic_tier_purchase'],
                conversionRate: 0.25
            },
            bundle: {
                name: 'Complete Bundle',
                description: 'Get all our products together at 40% off',
                price: 297,
                originalPrice: 495,
                conditions: ['single_product_purchase'],
                conversionRate: 0.2
            }
        };
        
        this.customerHistory = new Map();
    }
    
    async triggerUpsell(customerId, purchaseData) {
        const customer = await this.getCustomerProfile(customerId);
        const applicableOffers = this.getApplicableOffers(customer, purchaseData);
        
        if (applicableOffers.length === 0) {
            return null;
        }
        
        // Select best offer based on predicted conversion
        const bestOffer = this.selectBestOffer(applicableOffers, customer);
        
        // Present upsell
        const upsellResult = await this.presentUpsell(customer, bestOffer);
        
        // Track result
        await this.trackUpsellResult(customerId, bestOffer, upsellResult);
        
        return upsellResult;
    }
    
    getApplicableOffers(customer, purchaseData) {
        const offers = [];
        
        for (const [key, offer] of Object.entries(this.upsellOffers)) {
            if (this.checkConditions(offer.conditions, customer, purchaseData)) {
                offers.push({
                    ...offer,
                    key,
                    predictedConversion: this.predictConversion(offer, customer)
                });
            }
        }
        
        // Sort by predicted conversion rate
        return offers.sort((a, b) => b.predictedConversion - a.predictedConversion);
    }
    
    checkConditions(conditions, customer, purchaseData) {
        for (const condition of conditions) {
            switch(condition) {
                case 'immediate_post_purchase':
                    // Check if purchase just happened
                    const minutesSincePurchase = (Date.now() - purchaseData.timestamp) / (1000 * 60);
                    if (minutesSincePurchase > 15) return false;
                    break;
                    
                case 'basic_tier_purchase':
                    if (purchaseData.tier !== 'basic') return false;
                    break;
                    
                case 'single_product_purchase':
                    if (customer.totalPurchases > 1) return false;
                    break;
                    
                case 'high_value_customer':
                    if (customer.lifetimeValue < 500) return false;
                    break;
            }
        }
        
        return true;
    }
    
    predictConversion(offer, customer) {
        let baseRate = offer.conversionRate;
        
        // Adjust based on customer history
        if (customer.previousUpsellConversions > 0) {
            baseRate *= 1.2; // 20% higher if they've bought upsells before
        }
        
        if (customer.lifetimeValue > 1000) {
            baseRate *= 1.3; // 30% higher for high-value customers
        }
        
        // Time of day adjustment
        const hour = new Date().getHours();
        if (hour >= 9 && hour <= 17) {
            baseRate *= 1.1; // 10% higher during business hours
        }
        
        return Math.min(baseRate, 0.8); // Cap at 80%
    }
    
    selectBestOffer(offers, customer) {
        // Consider both conversion rate and profit
        const scoredOffers = offers.map(offer => ({
            ...offer,
            score: this.calculateOfferScore(offer, customer)
        }));
        
        return scoredOffers.sort((a, b) => b.score - a.score)[0];
    }
    
    calculateOfferScore(offer, customer) {
        const profit = offer.price * offer.predictedConversion;
        const customerSatisfactionImpact = this.estimateSatisfactionImpact(offer, customer);
        
        return (profit * 0.7) + (customerSatisfactionImpact * 0.3);
    }
    
    async presentUpsell(customer, offer) {
        // Create personalized upsell message
        const message = this.createUpsellMessage(customer, offer);
        
        // Present via appropriate channel
        let result;
        
        if (customer.onWebsite) {
            result = await this.presentModalUpsell(customer, message, offer);
        } else if (customer.email) {
            result = await this.sendEmailUpsell(customer, message, offer);
        }
        
        return result;
    }
    
    createUpsellMessage(customer, offer) {
        const templates = {
            immediate: `Hi ${customer.name}, since you just purchased ${customer.lastPurchase}, 
                      we're offering you ${offer.name} for ${offer.discount * 100}% off! 
                      This offer expires in ${offer.timeframe} minutes.`,
                      
            upgrade: `Hi ${customer.name}, you're currently using our Basic tier. 
                     Upgrade to ${offer.name} for just $${offer.price} more and get: 
                     ${offer.description}`,
                     
            bundle: `Hi ${customer.name}, you'll love our ${offer.name}! 
                    Get everything we offer at ${(1 - offer.price/offer.originalPrice) * 100}% off.`
        };
        
        return templates[offer.key.split('_')[0]] || templates.immediate;
    }
}
```

### Cross-Sell Recommendation Engine

**Intelligent Product Recommendations:**
```javascript
class RecommendationEngine {
    constructor() {
        this.products = {
            'ebook-ai': {
                name: 'AI Automation Ebook',
                category: 'education',
                price: 97,
                tags: ['ai', 'automation', 'beginner']
            },
            'templates-pro': {
                name: 'Professional Templates',
                category: 'tools',
                price: 147,
                tags: ['templates', 'advanced', 'time-saver']
            },
            'course-advanced': {
                name: 'Advanced AI Course',
                category: 'education',
                price: 297,
                tags: ['ai', 'advanced', 'video']
            },
            'consulting': {
                name: '1-on-1 Consulting',
                category: 'service',
                price: 997,
                tags: ['premium', 'personal', 'expert']
            }
        };
        
        this.customerProfiles = new Map();
        this.purchaseHistory = new Map();
    }
    
    async getRecommendations(customerId, context = {}) {
        const customer = await this.getCustomerProfile(customerId);
        const history = this.purchaseHistory.get(customerId) || [];
        
        // Multiple recommendation strategies
        const strategies = [
            this.contentBasedFiltering(customer, history),
            this.collaborativeFiltering(customerId),
            this.popularityBased(),
            this.contextBased(context)
        ];
        
        // Combine and rank recommendations
        const allRecs = [].concat(...strategies);
        const ranked = this.rankRecommendations(allRecs, customer);
        
        // Remove already purchased
        const purchasedIds = history.map(p => p.productId);
        const filtered = ranked.filter(rec => !purchasedIds.includes(rec.productId));
        
        // Return top 3
        return filtered.slice(0, 3);
    }
    
    contentBasedFiltering(customer, history) {
        // Recommend similar products to what they've bought/liked
        const recommendations = [];
        
        if (history.length > 0) {
            const lastProduct = history[history.length - 1];
            const product = this.products[lastProduct.productId];
            
            // Find products with similar tags
            for (const [id, p] of Object.entries(this.products)) {
                if (id === lastProduct.productId) continue;
                
                const similarity = this.calculateTagSimilarity(product.tags, p.tags);
                if (similarity > 0.3) {
                    recommendations.push({
                        productId: id,
                        product: p,
                        score: similarity * 0.7,
                        reason: `Similar to ${product.name}`,
                        strategy: 'content_based'
                    });
                }
            }
        }
        
        return recommendations;
    }
    
    collaborativeFiltering(customerId) {
        // "Customers who bought X also bought Y"
        const recommendations = [];
        const allHistory = Array.from(this.purchaseHistory.values()).flat();
        
        // Find customers with similar purchase patterns
        const similarCustomers = this.findSimilarCustomers(customerId);
        
        for (const similarCustomer of similarCustomers) {
            const theirPurchases = this.purchaseHistory.get(similarCustomer) || [];
            const myPurchases = this.purchaseHistory.get(customerId) || [];
            
            // Find products they bought that I didn't
            for (const purchase of theirPurchases) {
                if (!myPurchases.find(p => p.productId === purchase.productId)) {
                    const existing = recommendations.find(r => r.productId === purchase.productId);
                    
                    if (existing) {
                        existing.score += 0.1;
                        existing.reason = `Popular among customers like you`;
                    } else {
                        recommendations.push({
                            productId: purchase.productId,
                            product: this.products[purchase.productId],
                            score: 0.1,
                            reason: `Customers like you bought this`,
                            strategy: 'collaborative'
                        });
                    }
                }
            }
        }
        
        return recommendations;
    }
    
    popularityBased() {
        // Simply recommend popular products
        const purchaseCounts = new Map();
        
        // Count purchases for each product
        for (const history of this.purchaseHistory.values()) {
            for (const purchase of history) {
                purchaseCounts.set(
                    purchase.productId,
                    (purchaseCounts.get(purchase.productId) || 0) + 1
                );
            }
        }
        
        // Convert to recommendations
        return Array.from(purchaseCounts.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([productId, count]) => ({
                productId,
                product: this.products[productId],
                score: count / Math.max(...purchaseCounts.values()),
                reason: `Popular choice (${count} purchases)`,
                strategy: 'popularity'
            }));
    }
    
    contextBased(context) {
        // Recommend based on current context (time, location, device, etc.)
        const recommendations = [];
        const now = new Date();
        
